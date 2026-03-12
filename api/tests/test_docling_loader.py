import os
import sys

import pytest

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from api.core.rag.file_loader.docling_loader import DoclingLoader


@pytest.fixture
def loader():
    """Create a DoclingLoader instance for testing."""
    return DoclingLoader()


@pytest.fixture
def test_docx_path():
    """Get the path to the test DOCX file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "test_data", "doc1.docx")


def test_docling_loader_initialization(loader):
    """Test that DoclingLoader initializes correctly."""
    assert loader is not None
    assert hasattr(loader, "converter")
    assert hasattr(loader, "chunker")
    assert hasattr(loader, "supported_file_types")


def test_supported_file_types(loader):
    """Test that the loader reports correct supported file types."""
    supported = loader.supported_file_types
    
    assert isinstance(supported, list)
    assert len(supported) > 0
    
    # Check key formats are supported
    assert "docx" in supported
    assert "pdf" in supported
    assert "xlsx" in supported
    assert "md" in supported


def test_load_docx_file(loader, test_docx_path):
    """
    Test loading and parsing a DOCX file.
    
    This is the main test for doc1.docx processing.
    """
    # Verify test file exists
    assert os.path.exists(test_docx_path), f"Test file not found: {test_docx_path}"
    
    # Load the document
    documents = loader.load_file(test_docx_path)
    
    # Verify results
    assert documents is not None
    assert isinstance(documents, list)
    assert len(documents) > 0
    
    print(f"\n{'='*80}")
    print(f"Total chunks extracted: {len(documents)}")
    print(f"{'='*80}")
    
    # Check first few documents
    for i, doc in enumerate(documents[:5], 1):
        assert hasattr(doc, "page_content")
        assert hasattr(doc, "metadata")
        assert isinstance(doc.page_content, str)
        assert len(doc.page_content) > 0
        
        # Verify metadata contains reference
        assert "reference" in doc.metadata
        assert doc.metadata["reference"] == test_docx_path
        
        print(f"\n[Chunk {i}/{len(documents)}]")
        print(f"Length: {len(doc.page_content)} characters")
        print(f"Content preview: {doc.page_content[:100]}...")


def test_load_docx_content_structure(loader, test_docx_path):
    """Test that the loaded content has expected structure."""
    documents = loader.load_file(test_docx_path)
    
    # Combine all chunks to check overall content
    full_text = " ".join(doc.page_content for doc in documents)
    
    # Verify document contains expected Chinese legal text
    assert "第一章" in full_text or "第一条" in full_text
    assert len(full_text) > 100
    
    print(f"\n{'='*80}")
    print(f"Full document length: {len(full_text)} characters")
    print(f"First 200 characters:\n{full_text[:200]}")
    print(f"{'='*80}")


def test_load_nonexistent_file(loader):
    """Test that loading a nonexistent file raises FileNotFoundError."""
    fake_path = "/path/to/nonexistent/file.docx"
    
    with pytest.raises(FileNotFoundError) as exc_info:
        loader.load_file(fake_path)
    
    assert "does not exist" in str(exc_info.value)


def test_load_unsupported_file_type(loader, tmp_path):
    """Test that loading an unsupported file type raises ValueError."""
    # Create a temporary file with unsupported extension
    unsupported_file = tmp_path / "test.xyz"
    unsupported_file.write_text("test content")
    
    with pytest.raises(ValueError) as exc_info:
        loader.load_file(str(unsupported_file))
    
    assert "Unsupported file type" in str(exc_info.value)


def test_document_metadata_completeness(loader, test_docx_path):
    """Test that all documents have complete metadata."""
    documents = loader.load_file(test_docx_path)
    
    for doc in documents:
        # Check metadata structure
        assert "reference" in doc.metadata
        assert "text" in doc.metadata
        
        # Verify metadata values
        assert doc.metadata["reference"] == test_docx_path
        assert doc.metadata["text"] == doc.page_content


def test_chunking_consistency(loader, test_docx_path):
    """Test that chunking produces consistent results."""
    # Load the same file twice
    documents1 = loader.load_file(test_docx_path)
    documents2 = loader.load_file(test_docx_path)
    
    # Verify same number of chunks
    assert len(documents1) == len(documents2)
    
    # Verify content matches
    for doc1, doc2 in zip(documents1, documents2):
        assert doc1.page_content == doc2.page_content
        assert doc1.metadata["reference"] == doc2.metadata["reference"]
