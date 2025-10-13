const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage to simulate Adobe Experience Platform
let adobeData = [];

// Adobe Experience Platform API endpoints
app.post('/api/ingest', (req, res) => {
    try {
        const data = req.body;
        console.log('📥 Adobe AEP Ingest:', {
            id: data['@id'],
            email: data['xdm:identityMap']?.email?.[0]?.id,
            name: `${data['xdm:person']?.name?.firstName} ${data['xdm:person']?.name?.lastName}`.trim()
        });
        
        // Store in simulated Adobe data lake
        adobeData.push(data);
        
        res.json({
            success: true,
            message: 'Data ingested successfully into Adobe Experience Platform',
            recordId: data['@id']
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error ingesting data',
            error: error.message
        });
    }
});

app.get('/api/records', (req, res) => {
    res.json({
        success: true,
        count: adobeData.length,
        records: adobeData
    });
});

app.get('/api/health', (req, res) => {
    res.json({
        success: true,
        message: 'Adobe Experience Platform Simulator is running',
        timestamp: new Date().toISOString(),
        records: adobeData.length
    });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Adobe Experience Platform Simulator running on port ${PORT}`);
    console.log(`📊 Ready to receive Adobe SDFS data`);
});
