/**
 * Composable para a cena 3D do globo terrestre (WebGPU + Three.js).
 */
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three/webgpu'
import {
  step,
  normalWorld,
  output,
  texture,
  vec3,
  vec4,
  normalize,
  positionWorld,
  bumpMap,
  cameraPosition,
  color,
  uniform,
  mix,
  uv,
  max,
} from 'three/tsl'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { Timer } from 'three/addons/misc/Timer.js'

const TEXTURE_BASE = 'https://threejs.org/examples/textures/planets'

export function useEarthGlobe(containerRef) {
  const ready = ref(false)
  const error = ref(null)

  let renderer, scene, camera, controls, globe, timer, resizeHandler

  async function init() {
    const container = containerRef.value
    if (!container) return

    try {
      timer = new Timer()
      timer.connect(document)

      scene = new THREE.Scene()

      camera = new THREE.PerspectiveCamera(
        25,
        container.clientWidth / container.clientHeight,
        0.1,
        100,
      )
      camera.position.set(5.4, 0.6, 4.2)

      const sun = new THREE.DirectionalLight('#ffffff', 2)
      sun.position.set(0, 0, 3)
      scene.add(sun)

      const atmosphereDayColor = uniform(color('#4db2ff'))
      const atmosphereTwilightColor = uniform(color('#bc490b'))
      const roughnessLow = uniform(0.25)
      const roughnessHigh = uniform(0.35)

      const textureLoader = new THREE.TextureLoader()

      const dayTexture = textureLoader.load(`${TEXTURE_BASE}/earth_day_4096.jpg`)
      dayTexture.colorSpace = THREE.SRGBColorSpace
      dayTexture.anisotropy = 8

      const nightTexture = textureLoader.load(`${TEXTURE_BASE}/earth_night_4096.jpg`)
      nightTexture.colorSpace = THREE.SRGBColorSpace
      nightTexture.anisotropy = 8

      const bumpRoughnessCloudsTexture = textureLoader.load(
        `${TEXTURE_BASE}/earth_bump_roughness_clouds_4096.jpg`,
      )
      bumpRoughnessCloudsTexture.anisotropy = 8

      const viewDirection = positionWorld.sub(cameraPosition).normalize()
      const fresnel = viewDirection.dot(normalWorld).abs().oneMinus().toVar()
      const sunOrientation = normalWorld.dot(normalize(sun.position)).toVar()
      const atmosphereColor = mix(
        atmosphereTwilightColor,
        atmosphereDayColor,
        sunOrientation.smoothstep(-0.25, 0.75),
      )

      const globeMaterial = new THREE.MeshStandardNodeMaterial()
      const cloudsStrength = texture(bumpRoughnessCloudsTexture, uv()).b.smoothstep(0.2, 1)
      globeMaterial.colorNode = mix(texture(dayTexture), vec3(1), cloudsStrength.mul(2))

      const roughness = max(texture(bumpRoughnessCloudsTexture).g, step(0.01, cloudsStrength))
      globeMaterial.roughnessNode = roughness.remap(0, 1, roughnessLow, roughnessHigh)

      const night = texture(nightTexture)
      const dayStrength = sunOrientation.smoothstep(-0.25, 0.5)
      const atmosphereDayStrength = sunOrientation.smoothstep(-0.5, 1)
      const atmosphereMix = atmosphereDayStrength.mul(fresnel.pow(2)).clamp(0, 1)

      let finalOutput = mix(night.rgb, output.rgb, dayStrength)
      finalOutput = mix(finalOutput, atmosphereColor, atmosphereMix)
      globeMaterial.outputNode = vec4(finalOutput, output.a)

      const bumpElevation = max(texture(bumpRoughnessCloudsTexture).r, cloudsStrength)
      globeMaterial.normalNode = bumpMap(bumpElevation)

      const sphereGeometry = new THREE.SphereGeometry(1, 64, 64)
      globe = new THREE.Mesh(sphereGeometry, globeMaterial)
      globe.rotation.y = -0.8
      scene.add(globe)

      const atmosphereMaterial = new THREE.MeshBasicNodeMaterial({
        side: THREE.BackSide,
        transparent: true,
      })

      let alpha = fresnel.remap(0.73, 1, 1, 0).pow(3)
      alpha = alpha.mul(sunOrientation.smoothstep(-0.5, 1))
      atmosphereMaterial.outputNode = vec4(atmosphereColor, alpha)

      const atmosphere = new THREE.Mesh(sphereGeometry, atmosphereMaterial)
      atmosphere.scale.setScalar(1.04)
      scene.add(atmosphere)

      addStarfield(scene)
      addMoon(scene)
      addOrbitalRings(scene)

      renderer = new THREE.WebGPURenderer({ antialias: true, alpha: true })
      await renderer.init()
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
      renderer.setSize(container.clientWidth, container.clientHeight)
      renderer.setClearColor(0x000000, 0)
      container.appendChild(renderer.domElement)

      controls = new OrbitControls(camera, renderer.domElement)
      controls.enableDamping = true
      controls.enablePan = false
      controls.minDistance = 2.5
      controls.maxDistance = 12
      controls.autoRotate = true
      controls.autoRotateSpeed = 0.35
      controls.target.set(-0.65, -0.08, 0)

      resizeHandler = () => {
        if (!container || !renderer) return
        camera.aspect = container.clientWidth / container.clientHeight
        camera.updateProjectionMatrix()
        renderer.setSize(container.clientWidth, container.clientHeight)
      }
      window.addEventListener('resize', resizeHandler)

      renderer.setAnimationLoop(animate)
      ready.value = true
    } catch (err) {
      error.value = err?.message ?? 'WebGPU não disponível neste navegador.'
      console.error(err)
    }
  }

  function animate() {
    timer.update()
    const delta = timer.getDelta()
    globe.rotation.y += delta * 0.025
    controls.update()
    renderer.render(scene, camera)
  }

  function dispose() {
    window.removeEventListener('resize', resizeHandler)
    renderer?.setAnimationLoop(null)
    controls?.dispose()
    renderer?.dispose()
    if (containerRef.value && renderer?.domElement) {
      containerRef.value.removeChild(renderer.domElement)
    }
  }

  onMounted(init)
  onUnmounted(dispose)

  return { ready, error }
}

function addStarfield(scene) {
  const starGeo = new THREE.BufferGeometry()
  const starVerts = []
  for (let i = 0; i < 5000; i++) {
    const theta = Math.random() * Math.PI * 2
    const phi = Math.acos(2 * Math.random() - 1)
    const r = 35 + Math.random() * 25
    starVerts.push(
      r * Math.sin(phi) * Math.cos(theta),
      r * Math.sin(phi) * Math.sin(theta),
      r * Math.cos(phi),
    )
  }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(starVerts, 3))
  const starMat = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.06,
    transparent: true,
    opacity: 0.65,
  })
  scene.add(new THREE.Points(starGeo, starMat))
}

function addMoon(scene) {
  const moonGeo = new THREE.SphereGeometry(0.12, 32, 32)
  const moonMat = new THREE.MeshStandardNodeMaterial({
    color: 0x888888,
    roughness: 0.9,
  })
  const moon = new THREE.Mesh(moonGeo, moonMat)
  moon.position.set(3.8, 0.6, -2.5)
  scene.add(moon)
}

function addOrbitalRings(scene) {
  const ringMat = new THREE.LineBasicMaterial({
    color: 0x4db2ff,
    transparent: true,
    opacity: 0.12,
  })

  ;[1.55, 1.85, 2.15].forEach((radius, i) => {
    const points = []
    const segments = 128
    for (let j = 0; j <= segments; j++) {
      const angle = (j / segments) * Math.PI * 2
      points.push(new THREE.Vector3(Math.cos(angle) * radius, 0, Math.sin(angle) * radius))
    }
    const geo = new THREE.BufferGeometry().setFromPoints(points)
    const ring = new THREE.Line(geo, ringMat)
    ring.rotation.x = Math.PI / 2 + i * 0.08
    scene.add(ring)
  })
}
