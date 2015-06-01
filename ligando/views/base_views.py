from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import func, distinct, String
import simplejson as json
import pyopenms as oms

from ligando.models import (
    DBSession,
    Source,
    MsRun,
    Protein,
    HlaType,
    t_hla_map,
    SpectrumHit,
    t_spectrum_protein_map)
from ligando.views.view_helper import conn_err_msg, js_list_creator, js_list_creator_dataTables


@view_config(route_name='source', renderer='../templates/base_templates/source.pt', request_method="GET")
def source_page(request):
    try:
        # Catch if there are no peptides!!
        query = DBSession.query(func.count(SpectrumHit.spectrum_hit_id).label("count_hits"),
                                func.count(SpectrumHit.sequence.distinct()).label("count_pep"),
                                func.count(Protein.name.distinct()).label("count_prot")
        )
        query = query.join(Source)
        query = query.join(t_spectrum_protein_map)
        query = query.join(Protein)
        query = query.filter(Source.patient_id == request.matchdict["source"])
        statistics = json.dumps(query.all())

        query = DBSession.query(Source.patient_id,
                                func.group_concat(Source.histology.distinct().op('order by')(Source.histology)).label(
                                    'histology'),
                                func.group_concat(Source.source_id.distinct().op('order by')(Source.source_id)).label(
                                    'source_id'),
                                func.group_concat(Source.organ.distinct().op('order by')(Source.organ)).label(
                                    'organ'), func.group_concat(
                (Source.comment.distinct().op('order by')(Source.comment))).label(
                'comment'), func.group_concat(
                (Source.dignity.distinct().op('order by')(Source.dignity))).label(
                'dignity'),
                                func.group_concat(
                                    (Source.celltype.distinct().op('order by')(Source.celltype))).label(
                                    'celltype')
                                , func.group_concat(
                (Source.location.distinct().op('order by')(Source.location))).label(
                'location')
                                , func.group_concat(
                (Source.metastatis.distinct().op('order by')(Source.metastatis))).label(
                'metastatis'),
                                func.group_concat(
                                    (Source.person.distinct().op('order by')(Source.person))).label(
                                    'person'),
                                func.group_concat(
                                    (Source.organism.distinct().op('order by')(Source.organism))).label(
                                    'organism'),
                                func.group_concat(
                                    (HlaType.hla_string.distinct().op('order by')(HlaType.hla_string))).label(
                                    'hla_typing'),
                                func.group_concat(
                                    (Source.treatment.distinct().op('order by')(Source.treatment))).label(
                                    'treatment')
        )
        query = query.join(t_hla_map)
        query = query.join(HlaType)
        query = query.filter(Source.patient_id == request.matchdict["source"])
        query = query.group_by(Source.patient_id)
        metadata = json.dumps(query.all())

        query = DBSession.query(MsRun.ms_run_id, MsRun.filename).join(Source).filter(
            Source.patient_id == request.matchdict["source"])
        runs = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"statistic": statistics, "metadata": metadata, "runs": runs, "source": request.matchdict["source"]}


@view_config(route_name='source_id', renderer='../templates/base_templates/source_id.pt', request_method="GET")
def source_id_page(request):
    try:
        # Catch if there are no peptides!!
        query = DBSession.query(func.count(SpectrumHit.spectrum_hit_id).label("count_hits"),
                                func.count(SpectrumHit.sequence.distinct()).label("count_pep"),
                                func.count(Protein.name.distinct()).label("count_prot")
        )
        query = query.join(Source)
        query = query.join(t_spectrum_protein_map)
        query = query.join(Protein)
        query = query.filter(Source.source_id == request.matchdict["source_id"])
        statistics = json.dumps(query.all())

        query = DBSession.query(Source.source_id, func.group_concat(
            (Source.histology.distinct().op('order by')(Source.histology))).label(
            'histology')
                                , func.group_concat(
                (Source.patient_id.distinct().op('order by')(Source.patient_id))).label(
                'patient_id')
                                , func.group_concat(
                (Source.organ.distinct().op('order by')(Source.organ))).label(
                'organ')
                                , func.group_concat(
                (Source.comment.distinct().op('order by')(Source.comment))).label(
                'comment')
                                , func.group_concat(
                (Source.dignity.distinct().op('order by')(Source.dignity))).label(
                'dignity')
                                ,
                                func.group_concat(
                                    (Source.celltype.distinct().op('order by')(Source.celltype))).label(
                                    'celltype')
                                , func.group_concat(
                (Source.location.distinct().op('order by')(Source.location))).label(
                'location')
                                , func.group_concat(
                (Source.metastatis.distinct().op('order by')(Source.metastatis))).label(
                'metastatis')
                                ,
                                func.group_concat(
                                    (Source.person.distinct().op('order by')(Source.person))).label(
                                    'person')
                                , func.group_concat(
                (Source.organism.distinct().op('order by')(Source.organism))).label(
                'organism')
                                ,
                                func.group_concat(
                                    (HlaType.hla_string.distinct().op('order by')(HlaType.hla_string))).label(
                                    'hla_typing')
        )
        query = query.join(t_hla_map)
        query = query.join(HlaType)
        query = query.filter(Source.source_id == request.matchdict["source_id"])
        query = query.group_by(Source.source_id)
        metadata = json.dumps(query.all())

        query = DBSession.query(MsRun.ms_run_id, MsRun.filename).join(Source).filter(
            Source.source_id == request.matchdict["source_id"])
        runs = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"statistic": statistics, "metadata": metadata, "runs": runs, "source": request.matchdict["source_id"]}


@view_config(route_name='hla', renderer='../templates/base_templates/hla.pt', request_method="GET")
def hla_page(request):
    try:
        query = DBSession.query(Source.organ,Source.source_id, Source.dignity,
                                Source.histology, Source.patient_id)
        query = query.join(t_hla_map)
        query = query.join(HlaType)
        query = query.filter(HlaType.hla_string == request.matchdict["hla"])
        # * --> %2A cause * is reserved character
        # : --> %3A
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.join(t_hla_map)
        query = query.join(HlaType)
        query = query.filter(HlaType.hla_string == request.matchdict["hla"])
        statistic = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "hla": request.matchdict["hla"], "statistic": statistic}


@view_config(route_name='msrun', renderer='../templates/base_templates/msrun.pt', request_method="GET")
def msrun_page(request):
    try:
        query = DBSession.query(func.count(SpectrumHit.spectrum_hit_id).label("count_hits"),
                                func.count(SpectrumHit.sequence.distinct()).label("count_pep"),
                                func.count(Protein.name.distinct()).label("count_prot")
        )

        query = query.join(MsRun, SpectrumHit.ms_run_ms_run_id == MsRun.ms_run_id)
        query = query.join(t_spectrum_protein_map)
        query = query.join(Protein)
        query = query.filter(MsRun.ms_run_id == request.matchdict["msrun"])
        statistics = json.dumps(query.all())

        query = DBSession.query(MsRun.filename,
                                func.group_concat(
                                    (HlaType.hla_string.distinct().op('order by')(HlaType.hla_string))).label(
                                    'hla_typing'),
                                Source.histology, Source.source_id, Source.patient_id, Source.organ,
                                Source.comment, Source.dignity, Source.celltype, Source.location,
                                Source.metastatis, Source.person, Source.organism, Source.treatment, Source.comment.label("comment"),
                                func.cast(MsRun.ms_run_date, String).label("ms_run_date"), MsRun.used_share,
                                MsRun.comment.label("msrun_comment"),
                                MsRun.sample_mass, MsRun.sample_volume, MsRun.antibody_set,
                                MsRun.antibody_mass)
        query = query.join(Source)
        query = query.join(t_hla_map)
        query = query.join(HlaType)
        query = query.filter(MsRun.ms_run_id == request.matchdict["msrun"])
        metadata = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"statistics": statistics, "metadata": metadata, "msrun": request.matchdict["msrun"]}


@view_config(route_name='protein', renderer='../templates/base_templates/protein.pt', request_method="GET")
def protein_page(request):
    try:
        query = DBSession.query(Protein.name,
                                Protein.organism,
                                Protein.description,
                                Protein.sequence,
                                Protein.gene_name)
        query = query.filter(Protein.name == request.matchdict["protein"])
        temp_statistics = query.all()
        statistics = json.dumps(temp_statistics)
        query = DBSession.query(SpectrumHit.sequence.distinct())
        query = query.join(t_spectrum_protein_map)
        query = query.join(Protein)
        query = query.join(MsRun)
        query = query.filter(Protein.name == request.matchdict["protein"])
        query = query.filter(SpectrumHit.source_source_id != None)
        query = query.filter(MsRun.flag_trash ==0)
        sequences = query.all()
        # print sequences
        sequence_start = list()
        sequence_end = list()
        for seq in sequences:
            pos = temp_statistics[0][3].find(seq[0])
            if pos > -1:
                sequence_start.append(pos)
                sequence_end.append(pos + len(seq[0]))
        sequence_start = json.dumps(sequence_start)
        sequence_end = json.dumps(sequence_end)
        sequences = js_list_creator_dataTables(sequences)

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"statistics": statistics,
            "protein": request.matchdict["protein"],
            "sequence_start": sequence_start, "sequence_end": sequence_end, "sequences": sequences}


@view_config(route_name='organ', renderer='../templates/base_templates/organ.pt', request_method="GET")
def organ_page(request):
    try:
        query = DBSession.query(Source.source_id, Source.organ,
                                Source.histology, Source.patient_id, Source.dignity)
        query = query.filter(Source.organ == request.matchdict["organ"])
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.filter(Source.organ == request.matchdict["organ"])
        statistic = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "organ": request.matchdict["organ"], "statistic": statistic}


@view_config(route_name='person', renderer='../templates/base_templates/person.pt', request_method="GET")
def person_page(request):
    try:
        query = DBSession.query(Source.histology, Source.source_id, Source.patient_id, Source.organ,
                                Source.comment, Source.dignity, Source.celltype, Source.location,
                                Source.metastatis, Source.person, Source.organism)
        query = query.filter(Source.person == request.matchdict["person"])
        query = query.group_by(Source.source_id)
        sources = json.dumps(query.all())

        query = DBSession.query(MsRun.ms_run_id, MsRun.filename).join(Source).filter(
            Source.person == request.matchdict["person"])
        runs = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "runs": runs, "person": request.matchdict["person"]}


@view_config(route_name='peptide', renderer='../templates/base_templates/peptide.pt', request_method="GET")
def peptide_page(request):
    try:
        query = DBSession.query(Protein.name.label("protein"), Protein.gene_name.label("gene_name"))
        query = query.join(t_spectrum_protein_map)
        query = query.join(SpectrumHit)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.group_by(Protein.name)
        proteins = json.dumps(query.all())

        query = DBSession.query(Source.patient_id, Source.source_id)
        query = query.join(SpectrumHit)
        query = query.join(MsRun)
        #query = query.group_concat(MsRun)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.group_by(Source.patient_id)
        sources = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"proteins": proteins, "sources": sources,
            "peptide": request.matchdict["peptide"]}


# @view_config(route_name='peptide', renderer='../templates/base_templates/peptide.pt', request_method="GET")
@view_config(route_name='peptide_ajax', renderer='json', request_method="GET")
def specs(self):
    mi = "/home/walzer/ms-tools/UWPR-Lorikeet-742d110/140606_SW_MM1S_Pre#3_W_Adjusted#2_20%_Rep#5_25cm90min3s_msms70_indexed.mzML"
    si = 123
    imf_skip = oms.IndexedMzMLFile()
    imf_skip.setSkipXMLChecks(True)
    imf_skip.openFile(mi)
    if imf_skip.getParsingSuccess():
	    p = imf_skip.getSpectrumById(si);
	    mz = p.getMZArray()
	    inte = p.getIntensityArray()
    return {'sequence': 'AAAVPRAAF', 'peaks': zip(mz, inte)}


@view_config(route_name='histology', renderer='../templates/base_templates/histology.pt', request_method="GET")
def histology_page(request):
    try:
        query = DBSession.query(Source.source_id,Source.organ,
                                Source.dignity, Source.patient_id)
        query = query.filter(Source.histology == request.matchdict["histology"])
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.filter(Source.histology == request.matchdict["histology"])
        statistic = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "histology": request.matchdict["histology"], "statistic": statistic}


@view_config(route_name='celltype', renderer='../templates/base_templates/celltype.pt', request_method="GET")
def celltype_page(request):
    try:
        query = DBSession.query(Source.source_id, Source.organ, Source.dignity,
                                Source.histology, Source.patient_id)
        query = query.filter(Source.celltype == request.matchdict["celltype"])
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.filter(Source.celltype == request.matchdict["celltype"])
        statistic = json.dumps(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "celltype": request.matchdict["celltype"], "statistic": statistic}


@view_config(route_name='dignity', renderer='../templates/base_templates/dignity.pt', request_method="GET")
def dignity_page(request):
    try:
        query = DBSession.query(Source.source_id, Source.organ,
                                Source.histology, Source.patient_id,)
        query = query.filter(Source.dignity == request.matchdict["dignity"])
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.filter(Source.dignity == request.matchdict["dignity"])
        statistic = json.dumps(query.all())
    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "dignity": request.matchdict["dignity"], "statistic": statistic}


@view_config(route_name='location', renderer='../templates/base_templates/location.pt', request_method="GET")
def location_page(request):
    try:
        query = DBSession.query(Source.source_id, Source.organ,
                                Source.histology, Source.patient_id,Source.dignity)
        query = query.filter(Source.location == request.matchdict["location"])
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.filter(Source.location == request.matchdict["location"])
        statistic = json.dumps(query.all())
    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "location": request.matchdict["location"], "statistic": statistic}


@view_config(route_name='treatment', renderer='../templates/base_templates/treatment.pt', request_method="GET")
def treatment_page(request):
    try:
        query = DBSession.query(Source.organ, Source.source_id,
                                Source.treatment, Source.patient_id)
        query = query.filter(Source.treatment == request.matchdict["treatment"])
        sources = json.dumps(query.all())

        query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
        query = query.join(Source)
        query = query.filter(Source.treatment == request.matchdict["treatment"])
        statistic = json.dumps(query.all())
    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "treatment": request.matchdict["treatment"], "statistic": statistic}