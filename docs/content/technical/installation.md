# Installation


### Prerequisites

Before beginning the installation, ensure you have the following prerequisites installed on your system:

- Docker
- Docker Compose
- Git (optional, for cloning the repository)

### 1. Clone the Repository

If you have Git installed, you can clone the resmi repository directly. Alternatively, you can download the source code as a ZIP file from the GitHub repository.

```bash
git clone https://github.com/pomodoren/ResMI.git
cd ResMI
```

### 2. Setting Up the Environment

Navigate to the cloned repository and create a `.env` file by copying the example provided:

```bash
cp .env.example .env
```

Edit the `.env` file to set the necessary environment variables such as `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.

### 3. Launch the Services

Use Docker Compose to build and start the services:

```bash
docker-compose up -d
```

This command will start the following services based on the `docker-compose.yaml` configuration:

- **resmi:** The main application container.
- **resmi-db:** A PostgreSQL container for the database.

### 4. Verifying the Installation

After the containers are up and running, access the resmi application by navigating to `http://localhost:8080` in your web browser. This should load the resmi interface if the installation was successful.

### 5. Post-Installation Steps

After verifying that the installation is successful, you may need to perform initial setup tasks such as:

- Importing initial data
- Configuring additional settings through the resmi interface

### Troubleshooting

In case of errors during installation, check the Docker container logs for insights:

```bash
docker-compose logs
```
