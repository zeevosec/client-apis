"""Represent fhir entity."""

from anvil.transformers.fhir import join, make_identifier
from anvil.transformers.fhir.practitioner import Practitioner
from anvil.transformers.fhir.organization import Organization


class ResearchStudy:
    """Create fhir entity."""

    class_name = "research_study"
    resource_type = "ResearchStudy"

    @staticmethod
    def build_entity(workspace):
        """Create fhir entity."""
        print(workspace.keys())
        study_id = workspace["library:datasetName"]
        institution = workspace.institute
        investigator_name = workspace.study_pi
        study_name = workspace["library:datasetName"]
        attribution = workspace["library:datasetName"]
        short_name = workspace["library:datasetName"]
        key = workspace["library:datasetName"]

        entity = {
            "resourceType": ResearchStudy.resource_type,
            "id": make_identifier(study_id),
            "meta": {
                "profile": [
                    "http://fhir.kids-first.io/StructureDefinition/kfdrc-research-study"
                ]
            },
            "identifier": [
                {
                    "system": "https://kf-api-dataservice.kidsfirstdrc.org/studies?external_id=",
                    "value": study_id,
                },
                {
                    "system": "urn:kids-first:unique-string",
                    "value": join(ResearchStudy.resource_type, key),
                },
            ],
            "extension": [
                {
                    "url": "http://fhir.kids-first.io/StructureDefinition/related-organization",
                    "extension": [
                        {
                            "url": "organization",
                            "valueReference": {
                                "reference": f"Organization/{make_identifier(Organization.resource_type, institution)}"
                            },
                        }
                    ],
                }
            ],
            "title": study_name,
            "status": "completed",
            "principalInvestigator": {
                "reference": f"Practitioner/{make_identifier(Practitioner.resource_type, investigator_name)}"
            },
        }

        if attribution:
            entity["identifier"].append({"value": attribution})

        if short_name:
            entity["extension"].append(
                {
                    "url": "http://fhir.kids-first.io/StructureDefinition/display-name",
                    "valueString": short_name,
                }
            )

        return entity