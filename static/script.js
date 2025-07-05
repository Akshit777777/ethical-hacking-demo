
document.getElementById("dataForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    let data = {};
    formData.forEach((value, key) => data[key] = value);

    data.userAgent = navigator.userAgent;
    data.language = navigator.language;
    data.screen = `${window.screen.width}x${window.screen.height}`;
    data.colorDepth = window.screen.colorDepth;
    data.platform = navigator.platform;
    data.hardwareConcurrency = navigator.hardwareConcurrency;
    data.memory = navigator.deviceMemory || 'N/A';
    data.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    data.cookieEnabled = navigator.cookieEnabled;
    data.plugins = navigator.plugins.length;

    navigator.getBattery().then(battery => {
        data.battery = `${Math.round(battery.level * 100)}% (${battery.charging ? 'Charging' : 'Not Charging'})`;
        navigator.mediaDevices.enumerateDevices().then(devices => {
            data.devices = devices.map(d => d.kind + ': ' + (d.label || 'Unknown')).join(', ');
            // Use IP-based geolocation (no permission required)
            fetch("https://ipapi.co/json/")
              .then(res => res.json())
              .then(loc => {
                  data.ip_location = `${loc.city}, ${loc.region}, ${loc.country_name} (${loc.ip})`;
                  sendData(data);
              })
              .catch(() => {
                  data.ip_location = 'Unavailable';
                  sendData(data);
              });
        });
    });
});

function sendData(data) {
    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }).then(res => res.text()).then(alert);
}
