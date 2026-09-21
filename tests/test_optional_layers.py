import importlib

def test_ai_provider_import_is_dependency_free():
    module = importlib.import_module("src.ai.provider")
    assert module.get_provider().name == "none"

def test_pbr_schema_import_is_dependency_free():
    from src.pbr.schema import PBRTextureSet
    assert PBRTextureSet("crate").validate() == []

def test_mcp_namespace_import_is_dependency_free():
    importlib.import_module("src.mcp")
