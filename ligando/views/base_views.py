from sqlite3 import complete_statement
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import func, distinct, String, desc
import simplejson as json
from sqlalchemy import or_, func
from ligando.views.view_helper import get_chart_data


from ligando.models import (
    DBSession,
    Source,
    MsRun,
    Protein,
    HlaType,
    t_hla_map,
    SpectrumHit,
    t_spectrum_protein_map, Tissue_protein_count, Tissue_specific_peptides)
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

        #extract data for organ pie chart
        complete_sources = json.loads(sources)
        organ_chart = get_chart_data(complete_sources)


        # extract gene information
        query = DBSession.query(Protein.name,
                                Protein.organism,
                                Protein.description,
                                Protein.sequence,
                                Protein.gene_name)

        descriptor = request.matchdict["hla"].split("*")
        hla_description = descriptor[0] + descriptor[1].split(":")[0]

        query = query.filter(Protein.gene_name == "HLA-" + descriptor[0])
        query = query.filter(Protein.description.like("%" + hla_description + "%"))
        gene_information = json.dumps(query.all())


    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources, "hla": request.matchdict["hla"], "statistic": statistic, "genes": gene_information,
            "organ": organ_chart}


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

        if request.matchdict["type"] == "geneName":
            # TODO: a gene name is not unique!
            query = DBSession.query(Protein.name)
            query = query.filter(Protein.gene_name == request.matchdict["protein"])
            filter = query.one()[0]
        elif request.matchdict["type"] == "uniprot":
            filter = request.matchdict["protein"]
        else:
            return Response("Unknown Protein", content_type='text/plain', status_int=404)
        query = DBSession.query(Protein.name,
                                Protein.organism,
                                Protein.description,
                                Protein.sequence,
                                Protein.gene_name)
        query = query.filter(Protein.name == filter)
        temp_statistics = query.all()
        statistics = json.dumps(temp_statistics)
        query = DBSession.query(SpectrumHit.sequence.distinct())
        query = query.join(t_spectrum_protein_map)
        query = query.join(Protein)
        query = query.join(MsRun)
        query = query.filter(Protein.name == filter)
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
    # try:

    # TODO: Gene_name is not unique, but using Uniprot names is not understandable
    # Tissue specific proteins
    # class I
    query = DBSession.query(Tissue_protein_count.source_count, Protein.name, Protein.gene_name)
    query = query.order_by(desc(Tissue_protein_count.source_count))
    query = query.join(Protein)
    query = query.group_by(Protein.name)
    query = query.filter(Tissue_protein_count.tissue == request.matchdict["organ"])
    query = query.filter(Tissue_protein_count.hla_class == 1)
    query = query.filter(Tissue_protein_count.source_count > 1)
    # query = query.limit(50)
    protein_stats_classI = json.dumps(query.all())
    # class II
    query = DBSession.query(Tissue_protein_count.source_count, Protein.name, Protein.gene_name)
    query = query.order_by(desc(Tissue_protein_count.source_count))
    query = query.join(Protein)
    query = query.group_by(Protein.name)
    query = query.filter(Tissue_protein_count.tissue == request.matchdict["organ"])
    query = query.filter(Tissue_protein_count.hla_class == 2)
    query = query.filter(Tissue_protein_count.source_count > 1)
    # query = query.limit(50)
    protein_stats_classII = json.dumps(query.all())
    # combined
    query = DBSession.query(Tissue_protein_count.source_count, Protein.name, Protein.gene_name)
    query = query.order_by(desc(Tissue_protein_count.source_count))
    query = query.join(Protein)
    query = query.group_by(Protein.name)
    query = query.filter(Tissue_protein_count.tissue == request.matchdict["organ"])
    query = query.filter(Tissue_protein_count.hla_class == 0)
    query = query.filter(Tissue_protein_count.source_count > 1)
    # query = query.limit(50)
    protein_stats_combined = json.dumps(query.all())

    # Tissues specific PEPTIDES
    # class I
    query = DBSession.query(Tissue_specific_peptides.source_count, Tissue_specific_peptides.spectrum_hit_sequence)
    query = query.order_by(desc(Tissue_specific_peptides.source_count))
    query = query.group_by(Tissue_specific_peptides.spectrum_hit_sequence)
    query = query.filter(Tissue_specific_peptides.tissue == request.matchdict["organ"])
    query = query.filter(Tissue_specific_peptides.hla_class == 1)
    query = query.filter(Tissue_specific_peptides.source_count > 1)
    # query = query.limit(50)
    peptide_stats_classI = json.dumps(query.all())

    # class I
    query = DBSession.query(Tissue_specific_peptides.source_count, Tissue_specific_peptides.spectrum_hit_sequence)
    query = query.order_by(desc(Tissue_specific_peptides.source_count))
    query = query.group_by(Tissue_specific_peptides.spectrum_hit_sequence)
    query = query.filter(Tissue_specific_peptides.tissue == request.matchdict["organ"])
    query = query.filter(Tissue_specific_peptides.hla_class == 2)
    query = query.filter(Tissue_specific_peptides.source_count > 1)
    # query = query.limit(50)
    peptide_stats_classII = json.dumps(query.all())



    query = DBSession.query(Source.source_id, Source.organ,
                                Source.histology, Source.patient_id, Source.dignity)
    query = query.filter(Source.organ == request.matchdict["organ"])
    sources = json.dumps(query.all())

    # query = DBSession.query(func.count(SpectrumHit.sequence.distinct()).label("pep_count"))
    # query = query.join(Source)
    # query = query.filter(Source.organ == request.matchdict["organ"])
    # statistic = json.dumps(query.all())

    #except:
    #    return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"sources": sources,
            "organ": request.matchdict["organ"][0].upper() + request.matchdict["organ"][1:],
            # "statistic": statistic,
            "protein_stats_classI": protein_stats_classI,
            "protein_stats_classII": protein_stats_classII,
            "protein_stats_combined": protein_stats_combined,
            "peptide_stats_classI": peptide_stats_classI,
            "peptide_stats_classII": peptide_stats_classII

            }

@view_config(route_name='peptide', renderer='../templates/base_templates/peptide.pt', request_method="GET")
def peptide_page(request):
    try:
        query = DBSession.query(Protein.name.label("protein"), Protein.gene_name.label("gene_name"), Protein.sequence)
        query = query.join(t_spectrum_protein_map)
        query = query.join(SpectrumHit)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.group_by(Protein.name)
        proteins = json.dumps(query.all())

        # TODO: No trash run filtering, cause there will be no trash runs in the final DB
        # TODO: Makes no sense yet, cause for each run each peptide is only reported once!
        query = DBSession.query(func.count(SpectrumHit.spectrum_hit_id))
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        psms = query.all()[0][0]

        # TODO: No trash run filtering, cause there will be no trash runs in the final DB
        query = DBSession.query(func.count(SpectrumHit.ms_run_ms_run_id))
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        #query = query.group_by(SpectrumHit.sequence)
        #test = query.all()
        ms_run_count = query.all()[0][0]

        query = DBSession.query(Source.patient_id)
        query = query.join(SpectrumHit)
        query = query.join(MsRun)
        query = query.filter(MsRun.flag_trash ==0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.group_by(Source.patient_id)
        sources = js_list_creator_dataTables(query.all())

        #TODO: maybe sent one big query instead of many small ones
        query = DBSession.query(HlaType.hla_string.label("hla_class1_A"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(HlaType.hla_string.like("A%"))
        query = query.group_by(HlaType.hla_string)
        hla_class1_A = js_list_creator_dataTables(query.all())

        query = DBSession.query(HlaType.hla_string.label("hla_class1_B"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(
             HlaType.hla_string.like("B%"))
        query = query.group_by(HlaType.hla_string)
        hla_class1_B = js_list_creator_dataTables(query.all())

        query = DBSession.query(HlaType.hla_string.label("hla_class1_C"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(
            HlaType.hla_string.like("C%"))
        query = query.group_by(HlaType.hla_string)
        hla_class1_C = js_list_creator_dataTables(query.all())

        # TODO: there are probably more than these class 2 alleles
        query = DBSession.query(HlaType.hla_string.label("hla_class2_DPB"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(
            or_(HlaType.hla_string.like("DPB%")))
        query = query.group_by(HlaType.hla_string)
        hla_class2_DPB = js_list_creator_dataTables(query.all())

        query = DBSession.query(HlaType.hla_string.label("hla_class2_DQA"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(
            or_(HlaType.hla_string.like("DQA%")))
        query = query.group_by(HlaType.hla_string)
        hla_class2_DQA = js_list_creator_dataTables(query.all())

        query = DBSession.query(HlaType.hla_string.label("hla_class2_DQB"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(
            or_(HlaType.hla_string.like("DQB%")))
        query = query.group_by(HlaType.hla_string)
        hla_class2_DQB = js_list_creator_dataTables(query.all())

        query = DBSession.query(HlaType.hla_string.label("hla_class2_DRB"))
        query = query.join(t_hla_map)
        query = query.join(Source)
        query = query.join(SpectrumHit)
        query = query.filter(MsRun.flag_trash == 0)
        query = query.filter(SpectrumHit.sequence == request.matchdict["peptide"])
        query = query.filter(HlaType.digits == 4)
        query = query.filter(
            or_(HlaType.hla_string.like("DRB%")))
        query = query.group_by(HlaType.hla_string)
        hla_class2_DRB = js_list_creator_dataTables(query.all())

    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"proteins": proteins, "sources": sources,
            "peptide": request.matchdict["peptide"],
            "hla_class1_A": hla_class1_A, "hla_class1_B": hla_class1_B, "hla_class1_C": hla_class1_C,
            "hla_class2_DPB": hla_class2_DPB, "hla_class2_DQA": hla_class2_DQA, "hla_class2_DQB": hla_class2_DQB,
            "hla_class2_DRB": hla_class2_DRB, "psms": psms, "ms_run_count": ms_run_count}

