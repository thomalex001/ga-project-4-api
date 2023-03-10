from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductSerializer, PopulatedProductSerializer


class ProductListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        products = Product.objects.all() 
        serialized_products = PopulatedProductSerializer(products, many=True)
        return Response(serialized_products.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        product_to_add = ProductSerializer(data=request.data)
        try:
            product_to_add.is_valid()
            product_to_add.save()
            return Response(product_to_add.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProductDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)

        except Product.DoesNotExist:
            raise NotFound(detail="Can't find that product!")

    def get(self, _request, pk):
        product = self.get_product(pk=pk)
  
        serialized_product = ProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        product_to_edit = self.get_product(pk=pk)
        updated_product = ProductSerializer(product_to_edit, data=request.data)
        try:
            updated_product.is_valid()
            updated_product.save()
            return Response(updated_product.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            res = {
                "detail": "Unprocessable Entity"
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        print('DELETE ME')
        product_to_delete = self.get_product(pk=pk)
        product_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
