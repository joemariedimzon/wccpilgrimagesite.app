from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from wccpilgrimagesite.app import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import idnormalizer
from zope.app.container.interfaces import IObjectAddedEvent


# Interface class; used to define content-type schema.

class IPilgrimageSteps(form.Schema, IImageScaleTraversable):
    """
    Pilgrimage Steps
    """
#changed description to body
    form.widget(body=WysiwygFieldWidget)
    body = schema.Text(title=u"Description",
    required=False,
    )

    twitter_widget_id = schema.TextLine(
        title=u'Twitter widget ID',
        required=False,
        description=u'You may generate new twitter widget or edit existing one here: '
                    u'https://twitter.com/settings/widgets'
    )

    instagram_hashtags = schema.TextLine(
        title=u'Instagram hashtags',
        required=False,
        description=u'Please specify hashtags in a comma-separated list, e.g. #pilgrimage, #wcc. '
                    u'If you type @worldcouncilofchurches here, user feed would be displayed instead of '
                    u'hashtags.'
    )

    colour = schema.TextLine(
        title=u'Colour',
        required=True,
    )

    image = NamedBlobImage(
        title=u'Image',
        required=False,
    )


    pass

alsoProvides(IPilgrimageSteps, IFormFieldProvider)

@grok.subscribe(IPilgrimageSteps, IObjectAddedEvent)
def _createObj(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides = IPilgrimageSteps.__identifier__)
    for brain in brains:
        object_Ids.append(brain.id)
    
    last_name = str(idnormalizer.normalize(context.title))
    temp_new_id = last_name
    new_id = temp_new_id.replace("-","")
    test = ''
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        if '-' not in (max(test)):
            new_id = new_id + '-1'
        if '-' in (max(test)):
            new_id = new_id +'-' +str(int(max(test).split('-')[-1])+1) 

    parent.manage_renameObject(id, new_id )
    new_title = last_name
    context.setTitle(context.title)


    context.reindexObject()
    return


