from django.shortcuts import render
from django.views.generic import TemplateView

from applications.store.models import Product


class HomeView(TemplateView):
    template_name = 'index.html'  # Specify the template to render

    # Optional: Pass context data to the template
    def get_context_data(self, **kwargs):
        # Get the product by ID passed in the URL
        products = Product.objects.prefetch_related(
            'variants__variant_images'
        ).all()
        product_data = []
        for product in products:
            first_variant = product.variants.first()
            primary_image = None
            if first_variant:
                primary_image = first_variant.variant_images.filter(
                    is_primary=True).first()

            product_data.append({
                'product': product,
                'first_variant': first_variant,
                'primary_image': primary_image,
            })

        context = {'products': product_data}
        return context
