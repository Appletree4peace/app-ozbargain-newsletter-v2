const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { promisify } = require('util');
const exec = promisify(require('child_process').exec);

async function findChromiumExecutable() {
    try {
        // Adjust the command if necessary for your environment
        const { stdout } = await exec('which chromium-browser || which chromium');
        return stdout.trim(); // Remove newline character
    } catch (error) {
        console.error('Failed to find Chromium executable:', error);
        return null; // Or handle this case as needed
    }
}

async function takeScreenshot(filePath, outputPath) {
    const chromiumPath = await findChromiumExecutable();
    if (!chromiumPath) {
        console.log('Chromium executable not found. Please check your installation.');
        return;
    }

    const browser = await puppeteer.launch({
        headless: "new",
        executablePath: chromiumPath,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1256, height: 800 });

    const fileUrl = url.pathToFileURL(path.resolve(filePath)).toString();
    await page.goto(fileUrl, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: outputPath, fullPage: true });
    await browser.close();
}

async function screenshotHtmlFiles(baseFolder) {
    const htmlFiles = fs.readdirSync(baseFolder)
        .filter(file => file.startsWith('index_') && file.endsWith('.html'));

    for (const file of htmlFiles) {
        const filePath = path.join(baseFolder, file);
        const outputPath = path.join(baseFolder, `${path.parse(file).name}.png`);

        // Skip if screenshot already exists
        if (fs.existsSync(outputPath)) {
            console.log(`Screenshot already exists for ${file}, skipping...`);
            continue;
        }

        console.log(`Taking screenshot of ${file}`);
        await takeScreenshot(filePath, outputPath);
    }
}

const baseFolder = 'publish'; // Point to the publish folder
screenshotHtmlFiles(baseFolder)
    .then(() => console.log('All screenshots taken'))
    .catch(err => console.error('Error:', err));
