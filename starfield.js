// Get the canvas element
const canvas = document.getElementById('starfield');

// Create a WebGL renderer
const renderer = new THREE.WebGLRenderer({ canvas });

// Set the size of the renderer
renderer.setSize(window.innerWidth, window.innerHeight);

// Create a scene
const scene = new THREE.Scene();

// Create a camera
const camera = new THREE.PerspectiveCamera(100, window.innerWidth / window.innerHeight, 0.1, 10000);
camera.position.z = 1;

// Create stars
const starCount = 15000;
const geometry = new THREE.BufferGeometry();
const positions = [];
const colors = [];

// Define the color range and create random colors for the stars
for (let i = 0; i < starCount; i++) {
    // Position
    positions.push((Math.random() - 0.5) * 1500);
    positions.push((Math.random() - 0.5) * 1500);
    positions.push((Math.random() - 0.5) * 1500);
    
    // Color
    const color = new THREE.Color();
    color.setHSL(Math.random(), 1.0, 0.5); // HSL color space for variety
    colors.push(color.r, color.g, color.b);
}

// Create the position and color attributes
geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

// Create the PointsMaterial with vertexColors enabled and size set for circles
const material = new THREE.PointsMaterial({
    size: 2, // Adjust size for visibility
    vertexColors: true, // Enable per-vertex colors
    sizeAttenuation: true, // Optional: Make size attenuate with distance
    alphaTest: 0.5, // Optional: Control transparency if needed
    transparent: true // Optional: Enable transparency if using alphaTest
});

// Create the Points object and add it to the scene
const stars = new THREE.Points(geometry, material);
scene.add(stars);


// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Rotate the starfield
    stars.rotation.x += 0.0005;
    stars.rotation.y += 0.0005;

    // Move the camera
    camera.position.z -= 0.1;
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
