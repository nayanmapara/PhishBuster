![PhishBuster](https://user-images.githubusercontent.com/62838631/125227704-042d3780-e2f1-11eb-8f09-90ecd521f617.png)
<div align='center'>
<a href="https://www.codefactor.io/repository/github/vfxgamer/phishbuster"><img src="https://www.codefactor.io/repository/github/vfxgamer/phishbuster/badge" alt="CodeFactor" height="25"/></a>
<img src="https://img.shields.io/github/languages/code-size/VFXGamer/PhishBuster?style=for-the-badge" alt="GitHub code size in bytes" height="25"/></a>
<img src="https://img.shields.io/github/contributors/VFXGamer/PhishBuster?style=for-the-badge" alt="GitHub contributors" height="25"/></a>
<a href="https://deepsource.io/gh/VFXGamer/PhishBuster/?ref=repository-badge"><img src="https://deepsource.io/gh/VFXGamer/PhishBuster.svg/?label=active+issues&show_trend=true" alt="DeepSource" height="25"/></a>
</div>

## Sites:
For more details visit our [Blog](http://blog.cybervfx.tech/2021/06/phishbuster.html).<br>


## How to use 😀:

1. You just have to paste the url in the **ENTER THE SUSPECTED URL** section and **SELECT THE RESEMBELING SITE** it resembles or it is supposed to be and click on **START SCAN** and it will let you know it is a phishing site or not.

![home](https://user-images.githubusercontent.com/62838631/135703689-ff5cc34a-da02-42b7-8962-bce8abd1db49.jpg)

2. You can manually add phishing sites in [**reports**], click on add button to manually add phishing site.

![Manualadd](https://user-images.githubusercontent.com/62838631/135703691-d20235cc-cf45-4c92-bd1b-03fcf70d39ff.jpg)

3. You can go to **CONTRIBUTE** section and click on [**reports**] to see the list of all the phishing urls saved from the scans and manual add.

![contribute](https://user-images.githubusercontent.com/62838631/120368102-4b59fd00-c32f-11eb-978f-8dbffde01b61.png)

4. Report the phishing sites by clicking on the **report** button.

![reports](https://user-images.githubusercontent.com/62838631/135703692-0698eaa8-4903-4946-87c4-870e3b960f0f.jpg)

### PhishBuster API
Send a **POST** request to [PhishBuster Site](https://127.0.0.1:500/api/) and add *suspected link*, add the *site it is trying to refer to*, *your country* and *to store* the website URL if it is found to be a phishing site.<br>

**NOTE: You can use the following file** `call_api.py` **and send API request to the site.**

#### Steps:
1. Set **check-url** to the input url, **org-url** to original domain, **country** to your country and **store** to save the site in *reports* if it is phishing site.
2. You can run `python call_api.py` to use the PhishBuster API.
3. You will receive a *json* output with 5 fields *check-url*, *Original Url*, *Phishing Site* (boolean output), *country* and *save-scan-data*.

### Aim of the project is to reduce phishing victims. 😇
---
## License

Distributed under the MIT License. See [LICENSE](/LICENSE) for more information.

[**reports**]: https://phishbuster-web.herokuapp.com/reports
