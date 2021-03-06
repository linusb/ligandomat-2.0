import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,

    t_hla_map,
    HlaType,
    MsRun,
    t_peptide_protein_map,
    PeptideRun,
    t_peptide_run_spectrum_hit_map,
    Protein,
    Source,
    SpectrumHit,
    t_spectrum_protein_map
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    # with transaction.manager:
    # model = new_table_1(row1=1)
    #    DBSession.add(model)
