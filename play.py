from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch()
    page = browser.new_page()
    page.goto("https://www.tiktok.com/@MS4wLjABAAAAcnZpf_JE8RlAYTLsICDFB6CbPkqbfluOC2V4toocNAo/video/7057886142540172549?is_copy_url=1&is_from_webapp=v1&lang=es")
    page.screenshot(path="example.png")
    browser.close()
