# Online Courseware Downloader

**Online Coursewares don't need to be online anymore!**</br></br>
*This is the cheesiest tagline I could think of :)*

## Getting Started

This program helps you download online coursewares in the form of printable PDF files, which are viewable on a wide range of devices. Attempts have been made to preserve original quality of the lectures, without compromising the readability.

The actual courses are available [here](http://122.252.249.26:96/forms/frmlogin.aspx).

## Compatibility

Runs on 32bit and 64bit versions of Windows 7, 8, 8.1 and 10.

## How To

 - Download the latest windows binary executable from
   [the releases page](https://github.com/ankit1w/OCD/releases) and run it. 
   
  - The first run will trigger a Windows security alert, prompting whether or not
   to allow the main executable, as well as *phantomjs.exe* through the
   firewall. You can deny the firewall permissions, although
   it is recommended otherwise.
   
   - After selecting the subject of choice, the program will save its PDF in the same location as the executable.

## Bug reporting

> Before reporting bugs or readability issues, please cross check the OCD generated files with the actual coursewares available [here](http://122.252.249.26:96/forms/frmlogin.aspx). The program cannot fix bad formatting or missing files on the server side.

Report bugs via email at this address : [ankit.m@my.com](mailto:ankit.m@my.com?Subject=OCD%20Bug%20Report)

## Built With

* [PhantomJS](https://phantomjs.org/) - Headless browser used to scrape courseware site.
* [wkhtmltopdf](https://wkhtmltopdf.org/) - Command line tool to generate PDFs from HTML.
* [pdfCropMargins](https://github.com/abarker/pdfCropMargins) - Used to correct margins for easier readability, modified slightly to work without arguments.

## Acknowledgments

* Hat tip to anyone whose code was used.
* Thanks to the teachers who emphasized the importance of the Online Coursewares, which led me to develop this downloader instead of studying the lessons. :\
* [Stack Overflow](https://stackoverflow.com/), for being what it is.

## Donate

<p align="center">
  <a href="DONATE.md"><img width="250" height="150" src="https://www.svgrepo.com/show/194260/donate.svg"></a>
</p>
