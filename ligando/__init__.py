from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    #overview
    config.add_route('source_overview', '/sources')
    config.add_route('run_overview', '/runs')
    config.add_route('orphan_run_overview', '/orphan_runs')
    # DB query
    config.add_route('peptide_query', '/peptide_query')
    config.add_route('multi_peptide', '/multi_peptide')
    # upload page
    config.add_route('upload_metadata', '/upload_metadata')
    config.add_route('upload_metadata_source', '/upload_metadata_source')
    config.add_route('upload_metadata_ms_run', '/upload_metadata_ms_run')
    config.add_route('blacklist_msrun', '/blacklist_msrun')
    # base pages
    config.add_route('peptide', '/peptide/{peptide}')
    config.add_route('source', '/source/{source}')
    config.add_route('hla', '/hla/{hla}')
    config.add_route('msrun', '/msrun/{msrun}')
    config.add_route('protein', '/protein/{protein}')
    config.add_route('organ', '/organ/{organ}')
    config.add_route('celltype', '/celltype/{celltype}')
    config.add_route('histology', '/histology/{histology}')
    config.add_route('dignity', '/dignity/{dignity}')
    config.add_route('person', '/person/{person}')
    config.scan()
    return config.make_wsgi_app()
