from rest_framework import viewsets, status
from ..models import Product, Vendor, Customer, Category, Document, ProductList
from ..serializers import ProductSerializer, AddProductSerializer, SuccessSerializer
from ..serializers import ProductListSerializer, CreateProductListSerializer, DeleteProductListSerializer, ProductListAddProductSerializer, ProductListRemoveProductSerializer, ResponseSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from ..utils import create_product
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, JSONParser
from api.custom_permissions import IsAuthCustomer, IsAuthVendor


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductOptViewSet(viewsets.GenericViewSet):
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny, ]
    serializer_classes = {
        'add': AddProductSerializer
    }

    @swagger_auto_schema(method='post', responses={status.HTTP_201_CREATED: SuccessSerializer})
    @action(methods=['POST'], detail=False, permission_classes=[IsAuthVendor, ])
    def add(self, request):
        name = request.data.get("name")
        price = request.data.get("price")
        stock = request.data.get("stock")
        description = request.data.get("description")
        document = Document(upload=request.data.get("image_file"))
        document.save()
        image_file = document.upload
        category_name = request.data.get("category_name")
        category = Category.objects.get(name=category_name)
        vendor = Vendor.objects.filter(user=request.user).first()
        
        create_product(name=name, price=price, stock=stock, description=description,
                       image_url=image_file.url, category=category, vendor=vendor)

        return Response(data={'success': 'Successfully created product'}, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class ProductListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer


class ProductListOptViewSet(viewsets.GenericViewSet):
    parser_classes = (JSONParser,)
    permission_classes = [AllowAny, ]
    serializer_classes = {
        'add': CreateProductListSerializer,
        'delete': DeleteProductListSerializer,
        'add_product': ProductListAddProductSerializer,
        'remove_product': ProductListRemoveProductSerializer,
    }

    @swagger_auto_schema(method='post', responses={status.HTTP_201_CREATED: ResponseSerializer})
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthCustomer, ])
    def add(self, request):
        name = request.data.get("name")
        user = Customer(user=request.user)
        product_list = ProductList(name=name, user=user)
        product_list.save()
        return Response(data={'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(method='POST', responses={status.HTTP_200_OK: ResponseSerializer, status.HTTP_401_UNAUTHORIZED: ResponseSerializer})
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthCustomer, ])
    def delete(self, request):
        list_id = request.data.get("list_id")
        try:
            product_list = ProductList.objects.get(id=list_id)
        except ProductList.DoesNotExist:
            product_list = None

        if product_list is None:
            return Response(data={'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        user = Customer.objects.filter(user=request.user).first()
        if user is None or user != product_list.user:
            return Response(data={'ok': False}, status=status.HTTP_401_UNAUTHORIZED)
        product_list.delete()
        return Response(data={'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='POST', responses={status.HTTP_200_OK: ResponseSerializer, status.HTTP_401_UNAUTHORIZED: ResponseSerializer})
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthCustomer, ])
    def add_product(self, request):
        list_id = request.data.get("list_id")
        product_id = request.data.get("product_id")

        try:
            product_list = ProductList.objects.get(id=list_id)
        except ProductList.DoesNotExist:
            product_list = None

        if product_list is None:
            return Response(data={'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            product = None

        if product_list is None or product is None:
            return Response(data={'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        user = Customer.objects.filter(user=request.user).first()
        if user is None or user != product_list.user:
            return Response(data={'ok': False}, status=status.HTTP_401_UNAUTHORIZED)

        if product not in product_list.products.all():
            product_list.products.add(product)

        return Response(data={'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='POST', responses={status.HTTP_200_OK: ResponseSerializer, status.HTTP_401_UNAUTHORIZED: ResponseSerializer})
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthCustomer, ])
    def remove_product(self, request):
        list_id = request.data.get("list_id")
        product_id = request.data.get("product_id")
        try:
            product_list = ProductList.objects.get(id=list_id)
        except ProductList.DoesNotExist:
            product_list = None
        if product_list is None:
            return Response(data={'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            product = None
        if product_list is None or product is None:
            return Response(data={'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        user = Customer.objects.filter(user=request.user).first()
        if user is None or user != product_list.user:
            return Response(data={'ok': False}, status=status.HTTP_401_UNAUTHORIZED)
        product_list.products.remove(product)
        return Response(data={'ok': True}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
