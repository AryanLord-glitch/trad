/* ==============================
   TRAD – Particle Sphere Engine
   Clean & Stable Version
================================ */

window.addEventListener("load", initCanvas, false);

// ====== GLOBAL CONTROLS ======
let sphereRad = 140;
let radius_sp = 1;

// ====== INIT ======
function initCanvas() {
	const canvas = document.getElementById("canvasOne");
	if (!canvas) {
		console.error("Canvas not found");
		return;
	}

	const ctx = canvas.getContext("2d");
	const W = canvas.width;
	const H = canvas.height;

	// ====== PARTICLE SETTINGS ======
	const fLen = 320;
	const projCenterX = W / 2;
	const projCenterY = H / 2;
	const zMax = fLen - 2;

	let particleList = {};
	let recycleBin = {};

	const particleAlpha = 1;
	const particleRad = 1.8;
	const rgbString = "rgba(0,72,255,";

	const gravity = 0;
	const randAccel = 0.1;

	const sphereCenter = {
		x: 0,
		y: 0,
		z: -3 - sphereRad
	};

	const zeroAlphaDepth = -750;
	const turnSpeed = (2 * Math.PI) / 1200;
	let turnAngle = 0;

	let wait = 1;
	let count = 0;
	let numToAddEachFrame = 8;

	// ====== START LOOP ======
	setInterval(update, 1000 / 60);

	// ====== MAIN UPDATE ======
	function update() {
		count++;
		if (count >= wait) {
			count = 0;
			createParticles();
		}

		turnAngle = (turnAngle + turnSpeed) % (2 * Math.PI);
		const sinA = Math.sin(turnAngle);
		const cosA = Math.cos(turnAngle);

		ctx.fillStyle = "#000";
		ctx.fillRect(0, 0, W, H);

		let p = particleList.first;
		while (p) {
			let next = p.next;
			p.age++;

			if (p.age > p.stuckTime) {
				p.velX += randAccel * (Math.random() * 2 - 1);
				p.velY += gravity + randAccel * (Math.random() * 2 - 1);
				p.velZ += randAccel * (Math.random() * 2 - 1);

				p.x += p.velX;
				p.y += p.velY;
				p.z += p.velZ;
			}

			const rotX = cosA * p.x + sinA * (p.z - sphereCenter.z);
			const rotZ = -sinA * p.x + cosA * (p.z - sphereCenter.z) + sphereCenter.z;
			const m = radius_sp * fLen / (fLen - rotZ);

			p.projX = rotX * m + projCenterX;
			p.projY = p.y * m + projCenterY;

			updateAlpha(p);

			if (
				p.projX < 0 || p.projX > W ||
				p.projY < 0 || p.projY > H ||
				rotZ > zMax ||
				p.dead
			) {
				recycle(p);
			} else {
				const depthAlpha = Math.max(0, Math.min(1, 1 - rotZ / zeroAlphaDepth));
				ctx.fillStyle = rgbString + depthAlpha * p.alpha + ")";
				ctx.beginPath();
				ctx.arc(p.projX, p.projY, m * particleRad, 0, Math.PI * 2);
				ctx.fill();
			}

			p = next;
		}
	}

	// ====== PARTICLE CREATION ======
	function createParticles() {
		for (let i = 0; i < numToAddEachFrame; i++) {
			const theta = Math.random() * Math.PI * 2;
			const phi = Math.acos(Math.random() * 2 - 1);

			const x = sphereRad * Math.sin(phi) * Math.cos(theta);
			const y = sphereRad * Math.sin(phi) * Math.sin(theta);
			const z = sphereRad * Math.cos(phi);

			const p = addParticle(
				x,
				y,
				sphereCenter.z + z,
				0.002 * x,
				0.002 * y,
				0.002 * z
			);

			p.attack = 50;
			p.hold = 50;
			p.decay = 100;
			p.initValue = 0;
			p.holdValue = particleAlpha;
			p.lastValue = 0;
			p.stuckTime = 90 + Math.random() * 20;
		}
	}

	// ====== ALPHA ENVELOPE ======
	function updateAlpha(p) {
		if (p.age < p.attack) {
			p.alpha = (p.holdValue / p.attack) * p.age;
		} else if (p.age < p.attack + p.hold) {
			p.alpha = p.holdValue;
		} else if (p.age < p.attack + p.hold + p.decay) {
			p.alpha =
				p.holdValue -
				(p.holdValue / p.decay) * (p.age - p.attack - p.hold);
		} else {
			p.dead = true;
		}
	}

	// ====== PARTICLE MANAGEMENT ======
	function addParticle(x, y, z, vx, vy, vz) {
		let p = recycleBin.first || {};
		if (recycleBin.first) recycleBin.first = p.next;

		p.x = x;
		p.y = y;
		p.z = z;
		p.velX = vx;
		p.velY = vy;
		p.velZ = vz;
		p.age = 0;
		p.dead = false;

		p.next = particleList.first;
		if (particleList.first) particleList.first.prev = p;
		particleList.first = p;
		p.prev = null;

		return p;
	}

	function recycle(p) {
		if (p.prev) p.prev.next = p.next;
		if (p.next) p.next.prev = p.prev;
		if (particleList.first === p) particleList.first = p.next;

		p.next = recycleBin.first;
		recycleBin.first = p;
	}
}

/* ==============================
   TEXTILLATE (SAFE INIT)
================================ */
$(document).ready(function () {
	if ($(".tlt").length) {
		$(".tlt").textillate({
			in: { effect: "fadeInUp" }
		});
	}
});
