// Get the canvas element
const canvas = document.getElementById('starfield');

// Create a WebGL renderer
const renderer = new THREE.WebGLRenderer({ canvas });

// Set the size of the renderer
renderer.setSize(window.innerWidth, window.innerHeight);

// Create a scene
const scene = new THREE.Scene();

// Create a camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 1;

// Create stars
const starCount = 5000;
const geometry = new THREE.BufferGeometry();
const positions = [];

for (let i = 0; i < starCount; i++) {
    positions.push((Math.random() - 0.5) * 2000);
    positions.push((Math.random() - 0.5) * 2000);
    positions.push((Math.random() - 0.5) * 2000);
}

geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

// Create a material for the stars
const material = new THREE.PointsMaterial({ color: 0xffffff });

// Create a Points object and add it to the scene
const stars = new THREE.Points(geometry, material);
scene.add(stars);

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Rotate the starfield
    stars.rotation.x += 0.0005;
    stars.rotation.y += 0.0005;

    // Move the camera
    camera.position.z -= 0.05;
    if (camera.position.z < -1000) camera.position.z = 1;

    renderer.render(scene, camera);
}

animate();

// Handle window resize
window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});
