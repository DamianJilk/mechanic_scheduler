// Helper to fetch and populate mechanics dropdown
async function loadMechanics() {
    const res = await fetch('/api/mechanics');
    const mechanics = await res.json();
    const select = document.getElementById('select-mechanic');
    select.innerHTML = '';
    mechanics.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.id;
        opt.textContent = `${m.name} (${m.specialization || 'General'})`;
        select.appendChild(opt);
    });
}

// List appointments
async function loadAppointments() {
    const res = await fetch('/api/appointments');
    const appts = await res.json();
    const ul = document.getElementById('appointments');
    ul.innerHTML = '';
    appts.forEach(a => {
        const li = document.createElement('li');
        li.textContent = `${a.appointment_time}: ${a.mechanic_name} with ${a.customer_name} - ${a.description}`;
        ul.appendChild(li);
    });
}

// Event listeners
window.addEventListener('DOMContentLoaded', () => {
    loadMechanics();
    loadAppointments();

    document.getElementById('mechanic-form').addEventListener('submit', async e => {
        e.preventDefault();
        const name = document.getElementById('mech-name').value;
        const spec = document.getElementById('mech-spec').value;
        await fetch('/api/mechanics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, specialization: spec })
        });
        // TODO: handle errors and show success message
        document.getElementById('mech-name').value = '';
        document.getElementById('mech-spec').value = '';
        loadMechanics();
    });

    document.getElementById('appointment-form').addEventListener('submit', async e => {
        e.preventDefault();
        const mechanic_id = document.getElementById('select-mechanic').value;
        const customer_name = document.getElementById('cust-name').value;
        const appointment_time = document.getElementById('appt-time').value;
        const description = document.getElementById('appt-desc').value;
        // TODO: Create customer record or lookup existing
        // For MVP: create a new customer on the fly
        const custRes = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: customer_name })
        });
        const custData = await custRes.json();
        const customer_id = custData.id;

        await fetch('/api/appointments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mechanic_id, customer_id, appointment_time, description })
        });
        // TODO: error handling
        document.getElementById('cust-name').value = '';
        document.getElementById('appt-time').value = '';
        document.getElementById('appt-desc').value = '';
        loadAppointments();
    });
});