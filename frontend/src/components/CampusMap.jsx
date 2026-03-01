import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Text } from '@react-three/drei';

const BUILDINGS = [
    { id: 'Biotech_Block', position: [-8, 1.0, -8], size: [3, 2, 3] },
    { id: 'Canteen', position: [5, 0.5, -6], size: [4, 1, 4] },
    { id: 'Ground', position: [-9, 0.1, 0], size: [6, 0.2, 5] },  // Flat sports ground moved left
    { id: 'Hostel', position: [-6, 1.5, 8], size: [3, 3, 5] },
    { id: 'MB_Block', position: [0, 2.0, -1], size: [5, 4, 4] },
    { id: 'TP1', position: [7, 1.5, 2], size: [3, 3, 3] },
    { id: 'TP2', position: [10, 1.5, 8], size: [3, 3, 3] },
    { id: 'Auditorium', position: [-2, 1.0, -10], size: [6, 2.5, 5] },
];

const ROADS = [
    // Main horizontal boulevard
    { position: [0, 0.02, 1.5], size: [16, 2], rotation: [-Math.PI / 2, 0, 0] },
    // Main vertical boulevard
    { position: [3.5, 0.02, 0], size: [2, 12], rotation: [-Math.PI / 2, 0, 0] },
    // Path to Library
    { position: [-4, 0.02, -2], size: [2, 5], rotation: [-Math.PI / 2, 0, 0] },
    // Path to Hostel
    { position: [-2, 0.02, 3], size: [4, 1.5], rotation: [-Math.PI / 2, 0, 0] }
];

const GRASS_AREAS = [
    { position: [-4, 0.01, -0.5], size: [6, 2], rotation: [-Math.PI / 2, 0, 0] },
    { position: [0, 0.01, -3.5], size: [5, 5], rotation: [-Math.PI / 2, 0, 0] },
    { position: [6, 0.01, -2], size: [3, 8], rotation: [-Math.PI / 2, 0, 0] },
    { position: [-4, 0.01, 5], size: [6, 3], rotation: [-Math.PI / 2, 0, 0] },
];

function getZoneColor(status) {
    if (status === 'High Alert') return '#ef4444'; // red
    if (status === 'Moderate') return '#facc15'; // yellow
    return '#10b981'; // green
}

function getZoneGlow(status) {
    if (status === 'High Alert') return 2.0;
    if (status === 'Moderate') return 1.0;
    return 0.5;
}

function Building({ data, crowdData }) {
    const crowdInfo = crowdData.find(c => c.zone_id === data.id);
    const density = crowdInfo?.density || 0;
    const status = crowdInfo?.status || 'Normal';
    const color = getZoneColor(status);
    const glow = getZoneGlow(status);

    return (
        <group position={data.position}>
            {/* Main Building Body */}
            <mesh castShadow receiveShadow position={[0, 0, 0]}>
                <boxGeometry args={data.size} />
                <meshStandardMaterial
                    color="#1e293b"
                    roughness={0.7}
                    metalness={0.1}
                />
            </mesh>

            {/* Roof Detail - Sightly smaller and darker */}
            <mesh castShadow receiveShadow position={[0, data.size[1] / 2 + 0.05, 0]}>
                <boxGeometry args={[data.size[0] - 0.2, 0.1, data.size[2] - 0.2]} />
                <meshStandardMaterial color="#0f172a" roughness={0.9} />
            </mesh>

            {/* Glowing Window accents based on density */}
            <mesh position={[0, 0, data.size[2] / 2 + 0.02]}>
                <planeGeometry args={[data.size[0] - 0.5, data.size[1] - 0.2]} />
                <meshBasicMaterial color={color} transparent opacity={0.3 * glow} />
            </mesh>
            <mesh position={[0, 0, -data.size[2] / 2 - 0.02]} rotation={[0, Math.PI, 0]}>
                <planeGeometry args={[data.size[0] - 0.5, data.size[1] - 0.2]} />
                <meshBasicMaterial color={color} transparent opacity={0.3 * glow} />
            </mesh>

            {/* Glowing Heatmap Base Overlay */}
            <mesh position={[0, -data.size[1] / 2 + 0.1, 0]}>
                <boxGeometry args={[data.size[0] + 0.4, 0.2, data.size[2] + 0.4]} />
                <meshBasicMaterial color={color} transparent opacity={0.6 * glow} />
            </mesh>

            {/* Label */}
            <Text
                position={[0, data.size[1] / 2 + 0.8, 0]}
                fontSize={0.4}
                color="white"
                anchorX="center"
                anchorY="middle"
                outlineWidth={0.05}
                outlineColor="#000000"
            >
                {data.id}
            </Text>
            {/* Density Value */}
            {density > 0 && (
                <Text
                    position={[0, data.size[1] / 2 + 0.3, 0]}
                    fontSize={0.25}
                    color={color}
                    anchorX="center"
                    anchorY="middle"
                >
                    {Math.round(density)} pax
                </Text>
            )}
        </group>
    );
}

export default function CampusMap({ crowdData }) {
    return (
        <Canvas shadows camera={{ position: [10, 12, 12], fov: 45 }}>
            <color attach="background" args={['#0f172a']} />
            <fog attach="fog" args={['#0f172a', 10, 40]} />

            <ambientLight intensity={0.5} />
            <directionalLight
                position={[15, 20, 10]}
                intensity={1.2}
                castShadow
                shadow-mapSize-width={2048}
                shadow-mapSize-height={2048}
                shadow-bias={-0.0001}
            />

            {/* Main Ground Plane */}
            <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
                <planeGeometry args={[50, 50]} />
                <meshStandardMaterial color="#020617" roughness={1} metalness={0} />
            </mesh>

            {/* Grass Areas */}
            {GRASS_AREAS.map((g, i) => (
                <mesh key={`grass-${i}`} rotation={g.rotation} position={g.position} receiveShadow>
                    <planeGeometry args={g.size} />
                    <meshStandardMaterial color="#064e3b" roughness={1} metalness={0} opacity={0.3} transparent />
                </mesh>
            ))}

            {/* Roads */}
            {ROADS.map((r, i) => (
                <mesh key={`road-${i}`} rotation={r.rotation} position={r.position} receiveShadow>
                    <planeGeometry args={r.size} />
                    <meshStandardMaterial color="#334155" roughness={0.8} metalness={0.1} />
                </mesh>
            ))}

            {/* Grid Helper - Subtler */}
            <gridHelper args={[50, 50, '#1e293b', '#0f172a']} position={[0, 0.03, 0]} />

            {/* Buildings */}
            {BUILDINGS.map((b) => (
                <Building key={b.id} data={b} crowdData={crowdData} />
            ))}

            <OrbitControls
                makeDefault
                minPolarAngle={Math.PI / 6}
                maxPolarAngle={Math.PI / 2.1}
                minDistance={5}
                maxDistance={30}
            />
            <Environment preset="night" />
        </Canvas>
    );
}
