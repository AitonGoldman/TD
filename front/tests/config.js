exports.config = {    
    directConnect: true,
    framework: 'jasmine',  
    capabilities: {
        browserName: 'chrome'
    },
    specs: ['login_spec.js']
}