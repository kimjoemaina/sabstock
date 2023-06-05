from django.db import models
from django.db.models import Sum, F
from django.db import models
from core import settings
from django.conf import settings

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=125,verbose_name="Désignation")
    

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    reference = models.CharField(max_length=255)
    name = models.CharField(max_length=155, verbose_name="Désignation")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Catégorie")
    stinitial=models.IntegerField(verbose_name="Stock Initial")

    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    product = models.ForeignKey("Product", on_delete=models.CASCADE,verbose_name="Produit")


class Input(models.Model):
    date = models.DateField()

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_inputs",verbose_name="Produit"
    )
    unity = models.CharField(max_length=100,verbose_name="Unité")
    #initial_stock = models.IntegerField(null=True,verbose_name="Stock Initial")
    qty_input = models.IntegerField(verbose_name="Quantité entrée")
    source = models.CharField(max_length=100, verbose_name="Provenance")
    numeroCon=models.IntegerField(null=True, verbose_name="Numéro de Contenaire")
    bonrecept=models.CharField(null=True,max_length=100,verbose_name="Bon de Réception")
    comments=models.CharField(null=True,max_length=100,verbose_name="Commentaires")
    construction_site = models.ForeignKey(
        "ConstructionSite", on_delete=models.CASCADE, related_name="inputs"
    )


    class Meta:
        permissions = [
                ("export_inputs", "Can export inputs"),
                
            ]


class Output(models.Model):
    date = models.DateField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE,verbose_name="Produit")
    unity = models.CharField(max_length=100, verbose_name="Unité")
    qty_output = models.IntegerField(verbose_name="Quantité sortie")
    level = models.CharField(max_length=20,verbose_name="Niveau")
    appartment = models.CharField(max_length=20,verbose_name="Appartement")
    exit_coupon = models.IntegerField(verbose_name="N° Bon de sortie")
    construction_site = models.ForeignKey(
        "ConstructionSite", on_delete=models.CASCADE, related_name="outputs"
    )
    class Meta:
        permissions = [
                ("export_outputs", "Can export outputs"),
            ]


class ConstructionSite(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du chantier")

    def __str__(self) -> str:
        return self.name
    
    class Meta:
    
        permissions = [
                ("export_constructionsite", "Can export Construction Site"),
                ("see_dashboard", "Can See Dashboard"),
            ]

    # @property
    # def product(self):
    #     return self.input.all()[0].product.name
    @property
    def inputs_list_with_unique_products(self):
        data = self.inputs.filter(product__isnull=False).values("product").order_by("product").annotate(stock_input=Sum('qty_input'))
        return data

    @property
    def outputs_list_with_unique_products(self):
        data = (
            self.outputs.filter(product__isnull=False)
            .values("product")
            .order_by("product")
            .annotate(stock_output=Sum("qty_output"))
        )

        return data

    @property
    def merge_input_output(self):
        idata = self.inputs_list_with_unique_products
        odata = self.outputs_list_with_unique_products

        result = []
        for product in idata:
            try:
                pout = next(
                    item for item in odata if item["product"] == product["product"]
                )
            except:
                pout = None

            p = Product.objects.get(id=product["product"])
            product["stock_output"] = pout["stock_output"] if pout else 0
            # final_stock = (product["stock_input"] + p.stinitial) - pout["stock_output"] if pout else 0
            final_stock = (product["stock_input"] + p.stinitial) - product["stock_output"]
            product["final_stock"] = final_stock 
            p = Product.objects.get(id=product["product"])
            # product["product_instance"] = p
            product["category"] = p.category.name
            product["reference"] = p.reference
            product["product_name"] = p.name
            product["stinitial"] = p.stinitial
            
            stock_level_security = (10 / 100) * product["stock_input"]
            product["stock_level_security"] = round(stock_level_security, 2)

            if final_stock < stock_level_security:
                product[
                    "stock_state"
                ] = "<span style='color:red;'>Ré-Approvisionnement </span>"
            elif final_stock > stock_level_security:
                product["stock_state"] = "<span style='color:green;'>Niveau Satisfaisant</span>"
            else:
                product["stock_state"] = "None"

            result.append(product)


        return result


class ConstructionPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    constructionsite_permission = models.ManyToManyField(ConstructionSite)

    def __str__(self) -> str:
        return self.user.email



