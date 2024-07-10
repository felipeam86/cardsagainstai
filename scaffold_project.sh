#!/bin/bash

# Create backend structure
mkdir -p backend/app/{api/{routes,models,schemas},core,db,services,utils} backend/tests backend/alembic

# Create frontend structure
mkdir -p frontend/{public,src/{components,services,utils,styles}}

echo "Folder structure for Cards Against AI has been created!"
