import puppeteer from 'puppeteer';
(async () => {
  try {
    console.log("Launching browser...");
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    console.log("Navigating...");
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle0' });
    console.log("Done evaluating. Page title: ", await page.title());
    await browser.close();
  } catch (e) {
    console.error("Puppeteer error:", e);
  }
})();
