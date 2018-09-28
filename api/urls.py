"""SmartScreen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from api.views import *
from api.fin import *

urlpatterns = [
    url(r'^tanks/$', TankListInfoView.as_view()),
    url(r'^fuel/inventories/$', FuelInventoryListView.as_view()),
    url(r'^fuel/charge_times/$', FuelChargeTimesView.as_view()),
    url(r'^fuel/tanker_times/$', TankerSellTimesView.as_view()),
    url(r'^fuel/payments/$', FuelOrderPaymentView.as_view()),
    url(r'^fuel/sequential/$', FuelSequentialView.as_view()),
    url(r'^fuel/compare/$', FuelCompareYearView.as_view()),
    url(r'^fuel/composition/$', FuelCompositionView.as_view()),
    url(r'^fuel/detail/$', FuelCompareDetailView.as_view()),
    url(r'^fuel/predict/$', FuelSellPredict.as_view()),
    url(r'^fuel/plan/$', FuelSellPlanView.as_view()),
    url(r'^goods/payments/$', GoodsPaymentView.as_view()),
    url(r'^goods/sell/classification/$', GoodsClassificationSellView.as_view()),
    url(r'^goods/sell/rank/$', GoodsSellRankView.as_view()),
    url(r'^goods/guest/unit_price/$', GoodsGuestUnitPriceView.as_view()),
    url(r'^goods/guest/conversion/$', ConversionView.as_view()),
    url(r'^goods/product/effect/$', GoodsItemView.as_view()),
    url(r'^goods/month/sequential/$', GoodMonthSequentialView.as_view()),
    url(r'^goods/sequential/$', GoodSequentialView.as_view()),
    url(r'^goods/compare/$', GoodsCompareYearView.as_view()),
    url(r'^goods/unsold/$', UnsoldView.as_view()),
    url(r'^goods/fuel/compare/$', FuelGoodsCompareView.as_view()),
    url(r'^goods/search/month/sequential/$', GoodsSearchMonthSequentialView.as_view()),
    url(r'^goods/search/sequential/$', GoodsSearchSequentialView.as_view()),
    url(r'^goods/search/compare/$', GoodsSearchCompareYearView.as_view()),
    url(r'^goods/search/item/$', SearchListView.as_view()),
    url(r'^goods/overview/$', GoodsOverView.as_view()),
    url(r'^tool/daytime/$', DayTimeView.as_view()),
    url(r'^card/overview/$', CardOverView.as_view()),
    url(r'^card/composition/$', CardRecordTypeView.as_view()),
    url(r'^card/compare/$', CardRecordCompareView.as_view()),
    url(r'^cards/$', CardRecordListView.as_view()),
    url(r'^card/abnormal/$', AbnormalCardView.as_view()),
    url(r'^card/ranks/$', CardRankList.as_view()),
    url(r'^site/$', SiteInfoView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^messages/$', MessageView.as_view()),
    url(r'^overview/$', OverView.as_view()),
    url(r'^fin/income/osa/$', OilSellAmountView.as_view()),
    url(r'^fin/income/osm/$', OilSellMoneyView.as_view()),
    url(r'^fin/income/gsm/$', GoodsSellMoneyView.as_view()),
    url(r'^fin/cost/gsc/$', GasSellCostView.as_view()),
    url(r'^fin/cost/dsc/$', DieselSellCostView.as_view()),
    url(r'^fin/cost/gdsc/$', GoodsSellCostView.as_view()),
    url(r'^fin/cost/dc/$', DepreciationCostView.as_view()),
    url(r'^fin/cost/sc/$', SalaryCostView.as_view()),
    url(r'^fin/cost/dr/$', DailyRepairView.as_view()),
    url(r'^fin/cost/wec/$', WaterEleCostView.as_view()),
    url(r'^fin/cost/ol/$', OilLossView.as_view()),
    url(r'^fin/cost/oc/$', OtherCostView.as_view()),
    url(r'^fin/cost/tc/$', TotalCostView.as_view()),
    url(r'^fin/profit/ogp/$', OilGrossProfitView.as_view()),
    url(r'^fin/profit/tp/$', TotalProfitView.as_view()),
    url(r'^fin/profit/op/$', OilProfitView.as_view()),
    url(r'^fin/profit/gp/$', GoodsProfitView.as_view()),
    url(r'^fin/support/togp/$', TonOilGrossProfitView.as_view()),
    url(r'^fin/support/tggp/$', TonGasGrossProfitView.as_view()),
    url(r'^fin/support/tdgp/$', TonDieselGrossProfitView.as_view()),
    url(r'^fin/support/toc/$', TonOilCostView.as_view()),
    url(r'^fin/support/top/$', TonOilProfitView.as_view()),
    url(r'^fin/support/poa/$', PerOilAmountView.as_view()),
    url(r'^fin/support/pop/$', PerOilProfitView.as_view()),
    url(r'^fin/support/pgp/$', PerGoodsProfitView.as_view()),
    url(r'^fin/support/dsa/$', DailySellAmountView.as_view()),
    url(r'^fin/support/dagm/$', DailyAverageGoodsMoney.as_view()),
    url(r'^fin/use/bv/$', BalanceView.as_view()),

]
