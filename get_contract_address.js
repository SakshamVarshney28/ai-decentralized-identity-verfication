/**
 * Quick script to get the deployed contract address
 * Run: node get_contract_address.js
 */

const Web3 = require('web3');
const fs = require('fs');
const path = require('path');

async function getContractAddress() {
    try {
        // Connect to Ganache
        const web3 = new Web3('http://127.0.0.1:7545');
        
        if (!web3.utils.isAddress) {
            console.log('❌ Web3 not properly initialized');
            return;
        }
        
        // Check connection
        const isConnected = await web3.eth.isSyncing();
        console.log('✅ Connected to Ganache');
        
        // Get all accounts
        const accounts = await web3.eth.getAccounts();
        console.log(`📋 Found ${accounts.length} accounts`);
        
        // Get latest block
        const latestBlock = await web3.eth.getBlockNumber();
        console.log(`📦 Latest block: ${latestBlock}`);
        
        // Get transactions from latest blocks to find contract deployment
        console.log('\n🔍 Searching for deployed contracts...\n');
        
        let contractFound = false;
        
        // Check last 10 blocks for contract deployments
        for (let i = latestBlock; i >= Math.max(0, latestBlock - 10); i--) {
            try {
                const block = await web3.eth.getBlock(i, true);
                if (block && block.transactions) {
                    for (const tx of block.transactions) {
                        if (tx.to === null && tx.contractAddress) {
                            // This is a contract deployment
                            const code = await web3.eth.getCode(tx.contractAddress);
                            if (code !== '0x') {
                                console.log(`✅ Found deployed contract:`);
                                console.log(`   Address: ${tx.contractAddress}`);
                                console.log(`   Block: ${i}`);
                                console.log(`   Transaction: ${tx.hash}`);
                                console.log(`   From: ${tx.from}`);
                                console.log('');
                                contractFound = true;
                            }
                        }
                    }
                }
            } catch (e) {
                // Skip if block doesn't exist
            }
        }
        
        if (!contractFound) {
            console.log('❌ No deployed contracts found in recent blocks');
            console.log('   Please deploy the contract first:');
            console.log('   cd blockchain && npx truffle migrate --reset');
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        console.log('\n💡 Make sure:');
        console.log('   1. Ganache is running: npx ganache --port 7545');
        console.log('   2. Contract is deployed: cd blockchain && npx truffle migrate');
    }
}

// Run the function
getContractAddress();

