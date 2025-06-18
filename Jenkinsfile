pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.8'
        NODE_VERSION = '18'
        DOCKER_IMAGE_BACKEND = 'email-analyzer-backend'
        DOCKER_IMAGE_FRONTEND = 'email-analyzer-frontend'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    // Setup Python environment
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                    
                    // Setup Node.js environment
                    sh '''
                        cd web-frontend
                        npm install
                    '''
                }
            }
        }
        
        stage('Backend Tests') {
            steps {
                script {
                    sh '''
                        source venv/bin/activate
                        python -m pytest tests/ -v --cov=src --cov-report=xml
                    '''
                }
            }
            post {
                always {
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                }
            }
        }
        
        stage('Frontend Tests') {
            steps {
                script {
                    sh '''
                        cd web-frontend
                        npm run lint
                        npm run type-check
                        npm test -- --coverage --watchAll=false
                    '''
                }
            }
            post {
                always {
                    publishCoverage adapters: [lcovAdapter('web-frontend/coverage/lcov.info')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                }
            }
        }
        
        stage('Backend Build') {
            steps {
                script {
                    // Build backend executable for different platforms
                    sh '''
                        source venv/bin/activate
                        
                        # Build for Windows
                        python scripts/build_windows.py
                        
                        # Build for macOS
                        python scripts/build_macos.py
                        
                        # Build for Linux
                        python scripts/build_linux.py
                    '''
                }
            }
        }
        
        stage('Frontend Build') {
            steps {
                script {
                    sh '''
                        cd web-frontend
                        npm run build
                    '''
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    // Build backend Docker image
                    sh '''
                        docker build -t ${DOCKER_IMAGE_BACKEND}:${DOCKER_TAG} -f Dockerfile .
                        docker tag ${DOCKER_IMAGE_BACKEND}:${DOCKER_TAG} ${DOCKER_IMAGE_BACKEND}:latest
                    '''
                    
                    // Build frontend Docker image
                    sh '''
                        cd web-frontend
                        docker build -t ${DOCKER_IMAGE_FRONTEND}:${DOCKER_TAG} -f Dockerfile .
                        docker tag ${DOCKER_IMAGE_FRONTEND}:${DOCKER_TAG} ${DOCKER_IMAGE_FRONTEND}:latest
                    '''
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    // Scan Python dependencies
                    sh '''
                        source venv/bin/activate
                        safety check --json --output safety-report.json || true
                    '''
                    
                    // Scan Node.js dependencies
                    sh '''
                        cd web-frontend
                        npm audit --audit-level moderate --json > npm-audit-report.json || true
                    '''
                }
            }
            post {
                always {
                    publishJSON target: 'safety-report.json'
                    publishJSON target: 'web-frontend/npm-audit-report.json'
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                script {
                    // Start services for integration testing
                    sh '''
                        docker-compose up -d
                        sleep 30  # Wait for services to start
                        
                        # Run integration tests
                        source venv/bin/activate
                        python -m pytest tests/integration/ -v
                        
                        # Stop services
                        docker-compose down
                    '''
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    // Deploy to staging environment
                    sh '''
                        docker-compose -f docker-compose.staging.yml up -d
                    '''
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Deploy to production environment
                    sh '''
                        docker-compose -f docker-compose.prod.yml up -d
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup
            sh '''
                docker system prune -f
                rm -rf venv
            '''
            
            // Archive artifacts
            archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
            archiveArtifacts artifacts: 'web-frontend/.next/**/*', fingerprint: true
        }
        
        success {
            // Send success notification
            emailext (
                subject: "Email Box Analyzer Build #${env.BUILD_NUMBER} - SUCCESS",
                body: "Build completed successfully. Check the build at: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        
        failure {
            // Send failure notification
            emailext (
                subject: "Email Box Analyzer Build #${env.BUILD_NUMBER} - FAILED",
                body: "Build failed. Check the build at: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        
        cleanup {
            // Clean workspace
            cleanWs()
        }
    }
} 