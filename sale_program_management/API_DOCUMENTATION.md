# Sale Program Management API Documentation

## Base URL
```
http://your-odoo-server
```

## Authentication
All POST endpoints require authentication using API keys. Include the API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Authentication Test
**GET** `/api/sale_man/test-auth`
- **Description**: Debug endpoint to test authentication and view API keys
- **Authentication**: Not required
- **Response**: JSON with authentication debug information

### 2. Brands API

#### Get All Brands
**GET** `/api/sale_man/brands`
- **Description**: Retrieve all brands
- **Authentication**: Not required
- **Response**: 
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name_vi": "Brand Name VI",
      "name_en": "Brand Name EN",
      "code": "BR0001",
      "status": "active"
    }
  ]
}
```

#### Create Brand
**POST** `/api/sale_man/brands/create`
- **Description**: Create a new brand
- **Authentication**: Required
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_API_KEY`
- **Request Body**:
```json
{
  "name_vi": "Brand Name VI",
  "name_en": "Brand Name EN",
  "status": "active"
}
```
- **Response**:
```json
{
  "status": "success",
  "message": "Brand created successfully",
  "data": {
    "id": 1,
    "name_vi": "Brand Name VI",
    "name_en": "Brand Name EN",
    "code": "BR0001",
    "status": "active"
  }
}
```

### 3. Products API

#### Get All Products
**GET** `/api/sale_man/products`
- **Description**: Retrieve all products
- **Authentication**: Not required
- **Response**: 
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name_vi": "Product Name VI",
      "name_en": "Product Name EN",
      "code": "PRD0001",
      "status": "active",
      "category_id": 1,
      "brand_id": 1
    }
  ]
}
```

#### Create Product
**POST** `/api/sale_man/products/create`
- **Description**: Create a new product
- **Authentication**: Required
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_API_KEY`
- **Request Body**:
```json
{
  "name_vi": "Product Name VI",
  "name_en": "Product Name EN",
  "category_id": 1,
  "brand_id": 1,
  "status": "active"
}
```
- **Response**:
```json
{
  "status": "success",
  "message": "Product created successfully",
  "data": {
    "id": 1,
    "name_vi": "Product Name VI",
    "name_en": "Product Name EN",
    "code": "PRD0001",
    "status": "active",
    "category_id": 1,
    "brand_id": 1
  }
}
```

### 4. Categories API

#### Get All Categories
**GET** `/api/sale_man/categories`
- **Description**: Retrieve all categories
- **Authentication**: Not required
- **Response**: 
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name_vi": "Category Name VI",
      "name_en": "Category Name EN",
      "code": "CAT0001",
      "status": "active",
      "parent_id": null
    }
  ]
}
```

#### Create Category
**POST** `/api/sale_man/categories/create`
- **Description**: Create a new category
- **Authentication**: Required
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_API_KEY`
- **Request Body**:
```json
{
  "name_vi": "Category Name VI",
  "name_en": "Category Name EN",
  "parent_id": 1,
  "status": "active"
}
```
- **Response**:
```json
{
  "status": "success",
  "message": "Category created successfully",
  "data": {
    "id": 1,
    "name_vi": "Category Name VI",
    "name_en": "Category Name EN",
    "code": "CAT0001",
    "status": "active",
    "parent_id": 1
  }
}
```

### 5. Programs API

#### Get All Programs
**GET** `/api/sale_man/programs`
- **Description**: Retrieve all programs
- **Authentication**: Not required
- **Response**: 
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name_vi": "Program Name VI",
      "name_en": "Program Name EN",
      "code": "PRG0001",
      "status": "active",
      "start_date": "2024-01-01",
      "end_date": "2024-12-31",
      "company_id": 1
    }
  ]
}
```

#### Create Program
**POST** `/api/sale_man/programs/create`
- **Description**: Create a new program
- **Authentication**: Required
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer YOUR_API_KEY`
- **Request Body**:
```json
{
  "name_vi": "Program Name VI",
  "name_en": "Program Name EN",
  "company_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "status": "active"
}
```
- **Response**:
```json
{
  "status": "success",
  "message": "Program created successfully",
  "data": {
    "id": 1,
    "name_vi": "Program Name VI",
    "name_en": "Program Name EN",
    "code": "PRG0001",
    "status": "active",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "company_id": 1
  }
}
```

## Error Responses

All endpoints return standardized error responses:

```json
{
  "status": "error",
  "message": "Error description"
}
```

### Common HTTP Status Codes
- **200**: Success (GET requests)
- **201**: Created (POST requests)
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **403**: Forbidden (insufficient permissions)
- **500**: Internal Server Error

## Sequence Management

All models with `code` fields automatically generate codes using Odoo sequences:
- **Brands**: `BR0001`, `BR0002`, etc.
- **Products**: `PRD0001`, `PRD0002`, etc.
- **Categories**: `CAT0001`, `CAT0002`, etc.
- **Programs**: `PRG0001`, `PRG0002`, etc.

The sequence automatically continues from the highest existing number.

## Testing Examples

### Using curl

#### Test Authentication
```bash
curl -X GET http://your-odoo-server/api/sale_man/test-auth
```

#### Get All Brands
```bash
curl -X GET http://your-odoo-server/api/sale_man/brands
```

#### Create a Brand
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"name_vi": "Test Brand", "name_en": "Test Brand EN", "status": "active"}' \
  http://your-odoo-server/api/sale_man/brands/create
```

#### Create a Product
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"name_vi": "Test Product", "name_en": "Test Product EN", "category_id": 1, "brand_id": 1, "status": "active"}' \
  http://your-odoo-server/api/sale_man/products/create
```

### Using Postman

1. Set the request method (GET/POST)
2. Enter the URL
3. For POST requests:
   - Set `Content-Type: application/json` in Headers
   - Set `Authorization: Bearer YOUR_API_KEY` in Headers
   - Add JSON body in the Body tab
4. Send the request

## Notes

- All GET endpoints are public (no authentication required)
- All POST endpoints require API key authentication
- The `code` field is automatically generated and should not be provided in requests
- Date fields should be in ISO format (YYYY-MM-DD)
- Foreign key fields (like `category_id`, `brand_id`) should be provided as integers
- The `status` field accepts only "active" or "inactive" values 