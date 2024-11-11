import json
from django.core.management.base import BaseCommand
from unitrader.models import Media, Category, Landing, Navigation, Product, Review


class Command(BaseCommand):
    help = "Imports JSON data into the Django models"

    def handle(self, *args, **kwargs):
        with open("data.json", "r") as f:
            data = json.load(f)

        # Import media files
        media_mapping = {}
        for media_item in data["media"]:
            media = Media.objects.create(
                name=media_item["name"],
                original_name=media_item.get("original_name", ""),
                size=media_item.get("size", ""),
                type=media_item["type"],
                url=media_item.get("url", "https://placehold.co/600x400/png"),
                imgix_url=media_item.get("imgix_url", "https://placehold.co/600x400/png"),
                folder=media_item.get("folder", ""),
                created_at=media_item.get("created_at", ""),
                created_by="672472876bf9b88ef228c267",
            )
            media_mapping[media_item["name"]] = media  # Store for future references

        # # Import categories
        # for category_item in data["objects"]:
        #     if category_item["type_slug"] == "categories":
        #         category = Category.objects.create(
        #             slug=category_item["slug"],
        #             title=category_item["title"],
        #             description=category_item.get("content", ""),
        #             image=media_mapping.get(
        #                 category_item.get("metafields", [{}])[0].get("value")
        #             ),
        #         )

        # Import landing pages
        # for landing_item in data["objects"]:
        #     if landing_item["type_slug"] == "landings":
        #         print("I ran")
        #         landing = Landing.objects.create(
        #             slug=landing_item["slug"],
        #             title=landing_item["title"],
        #             description=landing_item.get("content", ""),
        #             hero_image=media_mapping.get(
        #                 landing_item.get("metafields", [{}])[0].get("value")
        #             ),
        #         )

        # Import navigation items
        # for navigation_item in data["objects"]:
        #     if navigation_item["type_slug"] == "navigation":
        #         navigation = Navigation.objects.create(
        #             slug=navigation_item["slug"],
        #             title=navigation_item["title"],
        #             link=navigation_item["content"],
        #             order=navigation_item["order"],
        #         )

        # Import products
        count1 =0
        count2 =0
        for product_item in data["objects"]:
            if product_item["type_slug"] == "products":
                count1 +=1
                categories = []
                for category_id in product_item.get("metafields", [{}])[0].get(
                    "value", []
                ):
                    try:
                        category = Category.objects.get(id=category_id)
                        categories.append(category)
                    except Exception as e:
                        print(e)
                        pass
                product = Product.objects.create(
                    slug=product_item["slug"],
                    title=product_item["title"],
                    image=media_mapping.get(
                        product_item.get("metafields", [{}])[0].get("value")
                    ),
                    description=product_item.get("metafields", [{}])[1].get("value"),
                    price=product_item.get("metafields", [{}])[2].get("value"),
                    count=product_item.get("metafields", [{}])[3].get("value"),
                    color=product_item.get("metafields", [{}])[4].get("value"),
                )
                count2 +=1

                product.category.set(categories)  # Set categories for product

        print(count1, count2)


        # Import reviews
        # for review_item in data["objects"]:
        #     if review_item["type_slug"] == "reviews":
        #         count1 +=1
        #         print(count1)
        #         product = Product.objects.get(
        #             slug=review_item["metafields"][0].get("value")
        #         )
        #         review = Review.objects.create(
        #             slug=review_item["slug"],
        #             product=product,
        #             title=review_item["title"],
        #             rating=review_item.get("metafields", [{}])[1].get("value"),
        #             content=review_item.get("content", ""),
        #         )

        self.stdout.write(
            self.style.SUCCESS("Successfully imported JSON data into Django models")
        )
