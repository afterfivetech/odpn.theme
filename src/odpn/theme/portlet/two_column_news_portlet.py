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
from plone.directives import form

class ITwoColumnsNewsPortlet(IPortletDataProvider):
    
    header_title = schema.TextLine(
        title = u"Portlet Header Title",
        required = True,
    )
    
    form.widget(first_column_source = 'plone.app.z3cform.wysiwyg.WysiwygFieldWidget')
    first_column_source = schema.Text(
        title = u"First Column Static Portlet",
        required = True,
        #source = CatalogSource(portal_type=('Topic', 'Collection'), default_query='path:'),
    )
    
    second_column_source = schema.Choice(
        title = u"Second Column Source Data",
        required = True,
        source = CatalogSource(portal_type=('Topic', 'Collection'), default_query='path:'),
    )
    
class Assignment(base.Assignment):
    implements(ITwoColumnsNewsPortlet)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @property
    def title(self):
        return self.header_title
    

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/two_column_news_portlet.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        
    def contents(self, column_name):
        data = self.data
        context = self.context
        column_source = getattr(data, column_name)
        results = []
        if column_source:
            uid = column_source
            brains = context.portal_catalog.searchResults(UID=uid)
            if brains:
                brain = brains[0]
                collection = context.unrestrictedTraverse(brain.getPath()).queryCatalog({'sort_on':'created',
                                                                                         'sort_order':'reverse',
                                                                                         'sort_limit':4})
                
                
                    
                datas = [coll for coll in collection]
                if datas:
                    datas.sort(key=lambda x: x.created, reverse=True)
                    results = datas[:4]
        
        return results
    
    
    def trim_description(self, value):
        if len(value) > 160:
            return value[:160]+' ...'
        return value
        

class AddForm(base.AddForm):
    schema = ITwoColumnsNewsPortlet
    #form_fields = form.Fields(ILatestBlogsPortlet)
    #fields = field.Fields(ILatestBlogsPortlet)
    
    label = u"Add Two Column Blogs/News Portlet"
    
    def create(self, data):
        return Assignment(**data)
    

class EditForm(base.EditForm):
    schema = ITwoColumnsNewsPortlet
    #form_fields = form.Fields(ILatestBlogsPortlet)
    #fields = field.Fields(ILatestBlogsPortlet)
    
    label = u"Edit Two Column Blogs/News Portlet"