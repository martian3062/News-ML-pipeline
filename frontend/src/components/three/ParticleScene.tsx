'use client';

import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function Particles({ count = 600 }: { count?: number }) {
  const mesh = useRef<THREE.Points>(null);

  const [positions, colors, sizes] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const sz = new Float32Array(count);

    // Crimson cloudy palette — warm, light tones
    const crimson = new THREE.Color('#dc2626');
    const rose = new THREE.Color('#e11d48');
    const rosegold = new THREE.Color('#b76e79');
    const blush = new THREE.Color('#fda4af');
    const palette = [crimson, rose, rosegold, blush];

    for (let i = 0; i < count; i++) {
      // Spread particles in a wide field
      pos[i * 3] = (Math.random() - 0.5) * 24;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 24;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 18;

      const color = palette[Math.floor(Math.random() * palette.length)];
      col[i * 3] = color.r;
      col[i * 3 + 1] = color.g;
      col[i * 3 + 2] = color.b;

      sz[i] = Math.random() * 3 + 0.5;
    }
    return [pos, col, sz];
  }, [count]);

  useFrame((state) => {
    if (!mesh.current) return;
    const time = state.clock.getElapsedTime();
    mesh.current.rotation.y = time * 0.015;
    mesh.current.rotation.x = Math.sin(time * 0.008) * 0.08;

    // Gentle floating
    const posArray = mesh.current.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      posArray[i3 + 1] += Math.sin(time * 0.2 + i * 0.08) * 0.0008;
    }
    mesh.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
        />
        <bufferAttribute
          attach="attributes-color"
          args={[colors, 3]}
        />
        <bufferAttribute
          attach="attributes-size"
          args={[sizes, 1]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.035}
        vertexColors
        transparent
        opacity={0.25}
        sizeAttenuation
        blending={THREE.NormalBlending}
        depthWrite={false}
      />
    </points>
  );
}

function ConnectionLines({ count = 50 }: { count?: number }) {
  const lines = useRef<THREE.LineSegments>(null);

  const positions = useMemo(() => {
    const pos = new Float32Array(count * 6);
    for (let i = 0; i < count; i++) {
      const i6 = i * 6;
      pos[i6] = (Math.random() - 0.5) * 16;
      pos[i6 + 1] = (Math.random() - 0.5) * 16;
      pos[i6 + 2] = (Math.random() - 0.5) * 12;
      pos[i6 + 3] = pos[i6] + (Math.random() - 0.5) * 3;
      pos[i6 + 4] = pos[i6 + 1] + (Math.random() - 0.5) * 3;
      pos[i6 + 5] = pos[i6 + 2] + (Math.random() - 0.5) * 3;
    }
    return pos;
  }, [count]);

  useFrame((state) => {
    if (!lines.current) return;
    lines.current.rotation.y = state.clock.getElapsedTime() * 0.012;
  });

  return (
    <lineSegments ref={lines}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
        />
      </bufferGeometry>
      <lineBasicMaterial
        color="#b76e79"
        transparent
        opacity={0.06}
        blending={THREE.NormalBlending}
      />
    </lineSegments>
  );
}

export default function ParticleScene() {
  return (
    <div className="canvas-container">
      <Canvas
        camera={{ position: [0, 0, 10], fov: 60 }}
        dpr={[1, 1.5]}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={0.2} />
        <Particles count={500} />
        <ConnectionLines count={35} />
      </Canvas>
    </div>
  );
}
