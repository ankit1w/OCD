# Online Courseware Downloader

## Getting Started

This program helps you download online coursewares in the form of printable PDF files, that can be viewed on a wide range of devices. Attempts have been made to preserve original quality of the lectures, without compromising the readability.

The actual courses are available [here](http://122.252.249.26:96/forms/frmlogin.aspx).

## Compatibility

Runs on 32-bit and 64-bit versions of Windows 7, 8, 8.1, 10 and 11.

## How To

 - Download the latest windows binary executable from
   [the releases page](https://github.com/ankit1w/OCD/releases) and run it. 
   
  - The first run will trigger a Windows security alert, prompting whether or not
   to allow the main executable, as well as *phantomjs.exe* through the
   firewall. You can deny the firewall permissions, although
   it is recommended otherwise.
   
   - After selecting the subject of choice, the program will save its PDF in the same location as the executable.
   
   
<p align="center">
  <img width="800" src="https://raw.githubusercontent.com/ankit1w/OCD/assets/ocd.gif">
</p> 

## Built With

* [PhantomJS](https://phantomjs.org/) - Headless browser used to scrape courseware site.
* [wkhtmltopdf](https://wkhtmltopdf.org/) - Command line tool to generate PDFs from HTML.
* [pdfCropMargins](https://github.com/abarker/pdfCropMargins) - Used to correct margins for easier readability, modified slightly to work without arguments.
