#!/usr/bin/env node
/**
 * Startup script for HCP CRM Vite Frontend
 */
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function installDependencies() {
    console.log('📦 Installing Vite frontend dependencies...');
    return new Promise((resolve, reject) => {
        const npm = spawn('npm', ['install'], {
            cwd: path.join(__dirname, 'hcp-crm-vite'),
            stdio: 'inherit',
            shell: true
        });
        
        npm.on('close', (code) => {
            if (code === 0) {
                console.log('✅ Dependencies installed successfully');
                resolve();
            } else {
                reject(new Error(`npm install failed with code ${code}`));
            }
        });
    });
}

function startViteDev() {
    console.log('🚀 Starting Vite development server...');
    const npm = spawn('npm', ['run', 'dev'], {
        cwd: path.join(__dirname, 'hcp-crm-vite'),
        stdio: 'inherit',
        shell: true
    });
    
    npm.on('close', (code) => {
        console.log(`Vite dev server exited with code ${code}`);
    });
}

function checkProjectExists() {
    const projectPath = path.join(__dirname, 'hcp-crm-vite');
    if (!fs.existsSync(projectPath)) {
        console.error('❌ hcp-crm-vite directory not found!');
        process.exit(1);
    }
}

async function main() {
    try {
        checkProjectExists();
        await installDependencies();
        startViteDev();
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

main();