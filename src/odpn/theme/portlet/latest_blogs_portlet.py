from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
#from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryMultiAdapter
from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.utils import getFSVersionTuple
from zope.schema.interfaces import IContextSourceBinder
from zope.component.hooks import getSite
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.vocabularies.catalog import CatalogSource

PLONE4 = getFSVersionTuple()[0] <= 4


class ILatestBlogsPortlet(IPortletDataProvider):
    
    header_title = schema.TextLine(
        title = u"Portlet Header Title",
        required = True,
    )
    
    source_data = schema.Choice(
        title = u"Source of Data",
        required = True,
        source = CatalogSource(portal_type=('Topic', 'Collection'), default_query='path:'),
    )
    

class Assignment(base.Assignment):
    implements(ILatestBlogsPortlet)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @property
    def title(self):
        return self.header_title
            

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/latest_blogs_portlet.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
    
    def contents(self):
        data = self.data
        context = self.context
        contents = {}
        results = []
        collection_path = ''
        
        if data.source_data:
            uid = data.source_data
            brains = context.portal_catalog.searchResults(UID=uid)
            if brains:
                brain = brains[0]
                
                collection = context.unrestrictedTraverse(brain.getPath()).queryCatalog({'sort_on':'created',
                                                                                         'sort_order':'reverse',
                                                                                         'sort_limit':4})
                
                
                if len(collection) > 5:
                    collection_path = collection_path = brain.getURL()
                datas = [coll for coll in collection]
                if datas:
                    datas.sort(key=lambda x: x.created, reverse=True)
                    results = datas[:4]
        contents = {'results':results, 'path':collection_path}
        return contents
    
    def trim_description(self, value):
        if len(value) > 160:
            return value[:160]+' ...'
        return value
    
class AddForm(base.AddForm):
    schema = ILatestBlogsPortlet
    #form_fields = form.Fields(ILatestBlogsPortlet)
    #fields = field.Fields(ILatestBlogsPortlet)
    
    label = u"Add Latest Blogs/News Portlet"
    
    def create(self, data):
        return Assignment(source_data = data.get('source_data', ''))
    

class EditForm(base.EditForm):
    schema = ILatestBlogsPortlet
    #form_fields = form.Fields(ILatestBlogsPortlet)
    #fields = field.Fields(ILatestBlogsPortlet)
    
    label = u"Edit Latest Blogs/News Portlet"
