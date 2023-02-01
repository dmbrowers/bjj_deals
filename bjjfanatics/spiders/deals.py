import scrapy
import re


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['bjjfanatics.com']
    start_urls = ['https://bjjfanatics.com/collections/daily-deals']

    def parse(self, response):
        deals = response.xpath("//a[@data-variation='original-product-card']")
        for deal in deals:
            product = deal.xpath(".//div/div[@class='product-card__name']/text()").get()
            link = deal.xpath(".//@href").get()
            original_price = deal.xpath(".//div/div/s[@class='product-card__regular-price']/text()").get()
            discounted_price = deal.xpath(".//div/div/s[@class='product-card__regular-price']/following-sibling"
                                          "::node()").get()
            image_url = deal.xpath(".//div/img").get()

            # Clean up the formatting of the fetched results
            absolute_url = f"https://bjjfanatics.com{link}"
            original_price = original_price.replace(" ", "").replace("$", "")
            discounted_price = discounted_price.replace(" ", "").replace("$", "")
            original_price = int(float(original_price))
            discounted_price = int(float(discounted_price))
            image_url = re.findall(r'src="(.*?)"', image_url)[0]
            image_url = f"http:{image_url}"

            # Determine the percentage discount
            discount_percentage = round(((original_price - discounted_price) / original_price) * 100)

            # Final formatting of $ and % values
            original_price = f"${original_price}"
            discounted_price = f"${discounted_price}"
            discount_percentage = f"{discount_percentage}%"

            yield {
                "product": product,
                "link": absolute_url,
                "original_price": original_price,
                "discounted_price": discounted_price,
                "discount": discount_percentage,
                "image_url": image_url
            }
