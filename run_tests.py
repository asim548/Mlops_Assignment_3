#!/usr/bin/env python
"""
Test Runner for APOD ETL Pipeline
Runs all unit tests and generates coverage report
"""

import subprocess
import sys
import os


def run_tests():
    """Run all tests with coverage"""
    
    print("=" * 60)
    print("🧪 APOD ETL Pipeline - Test Suite")
    print("=" * 60)
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("❌ pytest not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"], check=True)
    
    # Run tests
    print("\n📝 Running tests...\n")
    
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--cov=airflow/plugins/scripts",
            "--cov-report=html",
            "--cov-report=term-missing"
        ],
        cwd=os.path.dirname(__file__) or "."
    )
    
    print("\n" + "=" * 60)
    
    if result.returncode == 0:
        print("✅ All tests passed!")
        print("\n📊 Coverage report generated in: htmlcov/index.html")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
    
    print("=" * 60)


def validate_dag():
    """Validate DAG syntax"""
    
    print("\n" + "=" * 60)
    print("✓ Validating DAG syntax...")
    print("=" * 60)
    
    result = subprocess.run(
        [sys.executable, "airflow/dags/apod_etl_dag.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ DAG syntax is valid!")
    else:
        print("❌ DAG syntax error:")
        print(result.stderr)
        sys.exit(1)


def check_dependencies():
    """Check if all required packages are installed"""
    
    print("\n" + "=" * 60)
    print("📦 Checking dependencies...")
    print("=" * 60)
    
    required_packages = [
        "airflow",
        "pandas",
        "requests",
        "psycopg2",
        "dvc",
        "sqlalchemy",
        "dotenv",
        "pytest"
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


if __name__ == "__main__":
    try:
        # Check dependencies first
        if not check_dependencies():
            print("\n⚠️  Some dependencies are missing. Continue? (y/n)")
            if input().lower() != 'y':
                sys.exit(1)
        
        # Validate DAG
        validate_dag()
        
        # Run tests
        run_tests()
        
        print("\n🎉 All checks passed! Ready for deployment.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
