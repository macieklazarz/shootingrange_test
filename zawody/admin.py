from zawody.models import Zawody, Sedzia, Turniej, ZawodyDynamic, Druzyna, ZawodnicyDruzyny
from django.contrib import admin

# Register your models here.
@admin.register(Turniej)
class TurniejAdmin(admin.ModelAdmin):
	list_display = ('nazwa', 'rejestracja', 'klasyfikacja_generalna',)
	search_fields = ('nazwa',)

@admin.register(Sedzia)
class SedziaAdmin(admin.ModelAdmin):
	list_display = ('zawody','sedzia')
	search_fields = ('nazwa','sedzia')

@admin.register(Zawody)
class ZawodyAdmin(admin.ModelAdmin):
	list_display = ('nazwa', 'turniej',)
	search_fields = ('nazwa','turniej',)


@admin.register(ZawodyDynamic)
class ZawodyDynamicAdmin(admin.ModelAdmin):
	list_display = ('nazwa', 'turniej','miss','procedura','noshoot')
	search_fields = ('nazwa','turniej',)


@admin.register(Druzyna)
class Druzynadmin(admin.ModelAdmin):
	list_display = ('nazwa', 'administrator','turniej')
	search_fields = ('nazwa','administrator',)

@admin.register(ZawodnicyDruzyny)
class ZawodnicyDruzynydmin(admin.ModelAdmin):
	list_display = ('druzyna', 'zawodnik')
	search_fields = ('druzyna', 'zawodnik')