from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from django.db.models import Case, When, BooleanField, Value

class ProductFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__name',
        to_field_name='name',
        queryset=Tags.objects.all(),
        conjoined=False
    )
    product_type = filters.ModelMultipleChoiceFilter(
        field_name='product_type__name',
        to_field_name='name',
        queryset=ProductTypes.objects.all(),
    )
    colors = filters.ModelMultipleChoiceFilter(
        field_name='colors__name',
        to_field_name='name',
        queryset=Colors.objects.all(),
        conjoined=False
    )
    sizes = filters.ModelMultipleChoiceFilter(
        field_name='sizes__name',
        to_field_name='name',
        queryset=Sizes.objects.all(),
        conjoined=False
    )
    selling_price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['product_type', 'tags','selling_price','colors','sizes']


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):

        current_page = self.page.number
        page_links = self.get_html_context()["page_links"]

        section = int(current_page / 3) if current_page%3 !=0 else (current_page / 3 - 1)

        #creating which 3 will be rendered
        l = []
        for i in range(0,3):
            p = section*3 + i + 1
            if p <= self.page.paginator.num_pages:
                l.append(p)

        new_page_links = []
        for i,tu in enumerate(self.get_html_context()["page_links"]):
            if tu[1] in l:
                new_page_links.append(tu)

        html_context = self.get_html_context()
        html_context["page_links"] = new_page_links


        return Response({
            'html_context': html_context,
            'total_pages':self.page.paginator.num_pages,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class ProductAPI(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('product_type').prefetch_related('colors').prefetch_related('sizes').prefetch_related('tags').prefetch_related("product_images").all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['$product_type__name', '$title','$tags__name']
    ordering_fields = ['id', 'selling_price']
    ordering = ['-id']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.select_related('product_type').prefetch_related('colors').prefetch_related('sizes').prefetch_related('tags').prefetch_related("product_images")
        if self.request.user.is_authenticated:
            queryset.annotate(is_wishlisted=Case(
                When(wishlist_products__user=self.request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ))
        else:
            queryset.annotate(is_wishlisted=Value(False))
        return queryset


    @action(methods=['get'], detail=True)
    def get_product_details(self,request,pk=None):
        product = self.get_object()
        print(product.wishlist_products.all())
        print(product)
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)


    @action(methods=['get'], detail=False)
    def product_filters(self,request):
        pt_serializer = ProductTypeSerializer(ProductTypes.objects.all(), many=True)
        color_serializer = ColorsSerializer(Colors.objects.all(), many=True)
        size_serializer = SizesSerializer(Sizes.objects.all(), many=True)
        return Response([
            {
                "key":"product_type",
                "name":"Product Type",
                "values":pt_serializer.data
            },
            {
                "key":"colors",
                "name":"Color",
                "values":color_serializer.data
            },
            {
                "key":"sizes",
                "name":"Size",
                "values":size_serializer.data
            }
        ])

    # @action(methods=['get'], detail=False)
    # def get_popular_products(self,request):
    #     popular_products = Product.objects.all().order_by("-avg_rating")[0:6]
    #     serializer = ProductCardSerializer(popular_products,many=True)
    #     return Response(serializer.data)
    #
    # @action(methods=['get'], detail=False)
    # def get_delivery_details(self,request):
    #     start_pincode = "305001"
    #     pincode = request.GET['pincode']
    #     token="8288998bb6a27aa86fa341d6e26c03a8"
    #     end_point="https://test.sequel247.com/api/shipment/calculateEDD"
    #     todays_date = str(datetime.today().date())
    #     print(todays_date)
    #     data = {
    #         "origin_pincode": start_pincode,
    #         "destination_pincode": pincode,
    #         "pickup_date": todays_date,
    #         "token": token
    #     }
    #     r = requests.post(url = end_point, json = data)
    #     return Response(r.json())
