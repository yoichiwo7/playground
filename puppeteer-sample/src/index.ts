//import * as puppeteer from 'puppeteer';
const puppeteer = require('puppeteer');

const func = async () => {
  //const browser = await puppeteer.launch();
  const browser = await puppeteer.launch({headless: false, args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();

  await page.goto('https://google.com');
  await page.pdf({path: 'google.pdf'});

  await browser.close();
}

func()
