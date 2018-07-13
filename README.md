# CLNConfigure
A tool used to configure tags for CLN Helper

To utilize this tool a U of T login is required
Dependencies: Selenium, win32process, psutil

By itself this tool is useless, but it exists to improve the user experience for the CLNHelper application (still in prod).

At a highlevel it creates an instance of chrome, navigates to the CLN site, allows the user to configure what tags they want to target when applying for any job, then pulls those tags and saves to an external file.
