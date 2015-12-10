from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession, Base


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    # register static files in the static folder
    config.add_static_view('static', 'static', cache_max_age=3600)
    # home
    config.add_route('home', '/')
    # home search
    config.add_route('search', '/search')
    # overview
    config.add_route('source_overview', '/sources')
    config.add_route('run_overview', '/runs')
    config.add_route('orphan_run_overview', '/orphan_runs')
    # DB query
    config.add_route('peptide_query', '/peptide_query')
    # TODO: finish implementation
    config.add_route('multi_peptide', '/multi_peptide')
    # upload page
    #config.add_route('upload_metadata', '/upload_metadata')
    config.add_route('upload_metadata_source', '/upload_metadata_source')
    config.add_route('update_metadata_source', '/update_metadata_source')
    config.add_route('upload_metadata_ms_run', '/upload_metadata_ms_run')
    config.add_route('update_metadata_ms_run', '/update_metadata_ms_run')
    config.add_route('blacklist_msrun', '/blacklist_msrun')
    config.add_route('unblacklist_msrun', '/unblacklist_msrun')
    # base pages
    config.add_route('peptide', '/peptide/{peptide}')
    config.add_route('peptide_ajax', '/peptide_ajax/{peptide}')
    config.add_route('source', '/source/{source}')
    config.add_route('source_id', '/source_id/{source_id}')
    config.add_route('hla', '/hla/{hla}')
    config.add_route('msrun', '/msrun/{msrun}')
    config.add_route('protein', '/protein/{protein}')
    config.add_route('organ', '/organ/{organ}')
    config.add_route('celltype', '/celltype/{celltype}')
    config.add_route('histology', '/histology/{histology}')
    config.add_route('dignity', '/dignity/{dignity}')
    config.add_route('treatment', '/treatment/{treatment}')
    config.add_route('person', '/person/{person}')
    config.add_route('location', '/location/{location}')
    # Database analysis
    config.add_route('venn_analysis', '/venn_analysis')



    # test view TODO: remove before publishing
    config.add_route('test_view', '/test_view')
    # scan for views in whole project
    config.scan()
    return config.make_wsgi_app()
