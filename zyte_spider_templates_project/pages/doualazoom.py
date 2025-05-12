import re
from typing import List, Optional

from web_poet import field, WebPage
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class DoualazoomBasePage(WebPage):
    """Base class for all doualazoom.com pages."""
    
    @staticmethod
    def extract_text(el):
        """Extract text from a BeautifulSoup element."""
        return " ".join(el.stripped_strings) if el else ""


class DoualazoomListingPage(DoualazoomBasePage):
    """A company listing page on doualazoom.com."""
    
    BASE_URL = "https://www.doualazoom.com"
    
    @field
    def company_links(self) -> List[str]:
        """Extract company detail page links from the listing page."""
        soup = BeautifulSoup(self.html, "html.parser")
        anchors = soup.select("div.div_list_nomentreprise > a")
        return [urljoin(self.BASE_URL, a["href"]) for a in anchors if a.get("href")]
    
    @field
    def has_companies(self) -> bool:
        """Check if the listing page has any companies."""
        return len(self.company_links) > 0


class DoualazoomDetailPage(DoualazoomBasePage):
    """A company detail page on doualazoom.com."""
    
    @field
    def name(self) -> str:
        """Extract the company name."""
        soup = BeautifulSoup(self.html, "html.parser")
        name_el = soup.select_one("h2") or soup.select_one("h1")
        return self.extract_text(name_el) if name_el else soup.title.get_text(strip=True)
    
    @field
    def phones(self) -> List[str]:
        """Extract phone numbers."""
        soup = BeautifulSoup(self.html, "html.parser")
        phones = []
        for a in soup.select('a[href^="tel:"]'):
            num = a.get_text(strip=True)
            if "whatsapp" not in a.parent.get_text(" ").lower():
                phones.append(num)
        return phones
    
    @field
    def whatsapp(self) -> List[str]:
        """Extract WhatsApp numbers."""
        soup = BeautifulSoup(self.html, "html.parser")
        whatsapp = []
        for a in soup.select('a[href^="tel:"]'):
            num = a.get_text(strip=True)
            if "whatsapp" in a.parent.get_text(" ").lower():
                whatsapp.append(num)
        return whatsapp
    
    @field
    def emails(self) -> List[str]:
        """Extract email addresses."""
        soup = BeautifulSoup(self.html, "html.parser")
        return [a.get_text(strip=True) for a in soup.select('a[href^="mailto:"]')]
    
    @field
    def website(self) -> List[str]:
        """Extract external websites."""
        soup = BeautifulSoup(self.html, "html.parser")
        return [a["href"] for a in soup.select('a[href^="http"]')
                if "doualazoom.com" not in a["href"]]
    
    @field
    def localisation(self) -> str:
        """Extract company location."""
        soup = BeautifulSoup(self.html, "html.parser")
        loc_candidates = soup.find_all(text=re.compile(r"Localisation de l'entreprise|Situé à", re.I))
        return self.extract_text(loc_candidates[0].parent) if loc_candidates else ""
    
    @field
    def sectors(self) -> List[str]:
        """Extract business sectors."""
        soup = BeautifulSoup(self.html, "html.parser")
        return [self.extract_text(a) for a in soup.select('a[href*="/fr/activite/rubrique/"]')]
