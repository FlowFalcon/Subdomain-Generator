# Subdomain Creator

A web application built with Flask that allows users to easily create and manage subdomains through Cloudflare's API. This application features a modern, responsive UI with glass-effect design and animated elements.


## Live Demo

[https://subdomain-generator.flowfalcon.xyz](https://subdomain-generator.flowfalcon.xyz)


## Features

- Create DNS records (A, CNAME, TXT)
- Cloudflare proxy toggle support
- Multiple domain management
- Real-time feedback and notifications
- Modern glass-effect UI with animations
- Mobile-responsive design


## Project Structure

```
subdomain-creator/
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
├── wsgi.py
├── vercel.json
├── zones.json
└── README.md
```


## Prerequisites

- Python 3.6 or higher
- Cloudflare API key
- Registered domains on Cloudflare

## Installation

1. Clone the repository:
```bash
git clone https://github.com/FlowFalcon/Subdomain-Generator.git
cd Subdomain-Generator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your `zones.json` file:
```json
{
    "example.com": {
        "zone_id": "your_zone_id",
        "api_key": "your_api_key"
    }
}
```

## Running the Application

1. Local development:
```bash
python app.py
```
The application will be available at [http://localhost:8080](http://localhost:8080)

2. Using WSGI:
```bash
python wsgi.py
```



## Created By FlowFalcon
