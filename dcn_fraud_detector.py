
# src/services/meshNetwork.ts
mesh_network = """import { EventEmitter } from 'events';
import * as Network from 'expo-network';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface MeshNode {
  id: string;
  deviceId: string;
  lastSeen: number;
  signalStrength: number;
  hops: number;
}

interface DistressSignal {
  id: string;
  senderId: string;
  location: { latitude: number; longitude: number };
  timestamp: number;
  message: string;
  hopCount: number;
  relayPath: string[];
}

/**
 * Mesh Network Service
 * Handles peer-to-peer communication when cellular/WiFi is unavailable
 * Uses Bluetooth Low Energy and WiFi Direct for device-to-device relay
 */
export class MeshNetworkService extends EventEmitter {
  private static instance: MeshNetworkService;
  private isInitialized: boolean = false;
  private nearbyNodes: Map<string, MeshNode> = new Map();
  private distressCache: Map<string, DistressSignal> = new Map();
  private deviceId: string = '';
  private scanInterval: NodeJS.Timeout | null = null;

  static getInstance(): MeshNetworkService {
    if (!MeshNetworkService.instance) {
      MeshNetworkService.instance = new MeshNetworkService();
    }
    return MeshNetworkService.instance;
  }

  async initialize() {
    if (this.isInitialized) return;
    
    // Generate or retrieve device ID
    let storedId = await AsyncStorage.getItem('meshDeviceId');
    if (!storedId) {
      storedId = `dcn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      await AsyncStorage.setItem('meshDeviceId', storedId);
    }
    this.deviceId = storedId;

    // Start periodic scanning for nearby devices
    this.startScanning();
    
    this.isInitialized = true;
    console.log('Mesh network initialized:', this.deviceId);
  }

  /**
   * Start scanning for nearby mesh-capable devices
   */
  private startScanning() {
    // In a real implementation, this would use:
    // - react-native-ble-plx for Bluetooth LE scanning
    // - react-native-wifi-p2p for WiFi Direct discovery
    
    this.scanInterval = setInterval(async () => {
      const networkState = await Network.getNetworkStateAsync();
      
      // Only active mesh when no internet
      if (!networkState.isConnected) {
        await this.discoverPeers();
      }
    }, 30000); // Scan every 30 seconds
  }

  /**
   * Discover nearby peer devices
   */
  private async discoverPeers() {
    // Placeholder for BLE/WiFi Direct discovery
    // In production, this scans for other DCN apps broadcasting mesh beacons
    
    // Simulate finding peers for demo
    const mockPeers: MeshNode[] = [
      {
        id: 'peer_001',
        deviceId: 'dcn_device_001',
        lastSeen: Date.now(),
        signalStrength: -65,
        hops: 1,
      },
      {
        id: 'peer_002', 
        deviceId: 'dcn_device_002',
        lastSeen: Date.now(),
        signalStrength: -78,
        hops: 2,
      },
    ];

    mockPeers.forEach(peer => {
      this.nearbyNodes.set(peer.id, peer);
    });

    this.emit('peersUpdated', Array.from(this.nearbyNodes.values()));
  }

  /**
   * Broadcast distress signal to mesh network
   */
  async broadcastDistress(location: { latitude: number; longitude: number }, message: string): Promise<number> {
    const signal: DistressSignal = {
      id: `distress_${Date.now()}`,
      senderId: this.deviceId,
      location,
      timestamp: Date.now(),
      message,
      hopCount: 0,
      relayPath: [this.deviceId],
    };

    // Store locally
    this.distressCache.set(signal.id, signal);
    await this.persistDistressSignal(signal);

    // Relay to all nearby nodes
    let relayCount = 0;
    for (const [peerId, node] of this.nearbyNodes) {
      if (node.hops <= 3) { // Max 3 hops
        try {
          await this.relayToPeer(peerId, signal);
          relayCount++;
        } catch (err) {
          console.error(`Failed to relay to ${peerId}:`, err);
        }
      }
    }

    this.emit('distressBroadcast', { signal, relayCount });
    return relayCount;
  }

  /**
   * Relay distress signal to a specific peer
   */
  private async relayToPeer(peerId: string, signal: DistressSignal): Promise<void> {
    const relayedSignal = {
      ...signal,
      hopCount: signal.hopCount + 1,
      relayPath: [...signal.relayPath, this.deviceId],
    };

    // In production, this sends via BLE or WiFi Direct
    console.log(`Relaying distress to ${peerId}:`, relayedSignal);
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  /**
   * Scan for incoming distress signals from mesh
   */
  async scanForDistressSignals(): Promise<DistressSignal[]> {
    // In production, this listens for BLE advertisements or WiFi Direct broadcasts
    // For now, check persisted signals from storage
    
    const stored = await AsyncStorage.getItem('meshDistressSignals');
    const signals: DistressSignal[] = stored ? JSON.parse(stored) : [];
    
    // Filter for unacknowledged signals
    const activeSignals = signals.filter(s => 
      Date.now() - s.timestamp < 3600000 // Within last hour
    );

    if (activeSignals.length > 0) {
      this.emit('distressReceived', activeSignals);
    }

    return activeSignals;
  }

  /**
   * Acknowledge a distress signal (stop relaying)
   */
  async acknowledgeDistress(signalId: string): Promise<void> {
    const signal = this.distressCache.get(signalId);
    if (signal) {
      signal.relayPath.push('ACK');
      await this.persistDistressSignal(signal);
    }
  }

  /**
   * Get nearby mesh nodes
   */
  getNearbyNodes(): MeshNode[] {
    return Array.from(this.nearbyNodes.values());
  }

  /**
   * Check if mesh network is available
   */
  isMeshAvailable(): boolean {
    return this.nearbyNodes.size > 0;
  }

  /**
   * Persist distress signal to storage
   */
  private async persistDistressSignal(signal: DistressSignal): Promise<void> {
    const stored = await AsyncStorage.getItem('meshDistressSignals');
    const signals: DistressSignal[] = stored ? JSON.parse(stored) : [];
    
    const existingIndex = signals.findIndex(s => s.id === signal.id);
    if (existingIndex >= 0) {
      signals[existingIndex] = signal;
    } else {
      signals.push(signal);
    }
    
    // Keep only last 50 signals
    if (signals.length > 50) signals.shift();
    
    await AsyncStorage.setItem('meshDistressSignals', JSON.stringify(signals));
  }

  /**
   * Send message through mesh to a specific destination
   */
  async sendMeshMessage(destinationId: string, payload: any): Promise<boolean> {
    // Find route to destination
    const route = this.findRoute(destinationId);
    if (!route || route.length === 0) return false;

    // Send hop by hop
    let currentPayload = payload;
    for (const hopId of route) {
      currentPayload = await this.forwardMessage(hopId, currentPayload);
    }

    return true;
  }

  /**
   * Find shortest route to destination using simple hop counting
   */
  private findRoute(destinationId: string): string[] | null {
    // Simplified routing - in production, use proper mesh routing algorithm
    const destNode = this.nearbyNodes.get(destinationId);
    if (!destNode) return null;
    
    // Direct connection
    if (destNode.hops === 1) return [destinationId];
    
    // Multi-hop: find intermediate nodes
    const intermediates = Array.from(this.nearbyNodes.values())
      .filter(n => n.hops < destNode.hops);
    
    if (intermediates.length > 0) {
      return [intermediates[0].id, destinationId];
    }
    
    return null;
  }

  private async forwardMessage(peerId: string, payload: any): Promise<any> {
    console.log(`Forwarding message to ${peerId}`);
    return payload;
  }

  cleanup() {
    if (this.scanInterval) {
      clearInterval(this.scanInterval);
    }
    this.nearbyNodes.clear();
    this.distressCache.clear();
  }
}
"""

with open(f'{app_dir}/src/services/meshNetwork.ts', 'w') as f:
    f.write(mesh_network)

# src/services/backgroundTasks.ts
bg_tasks = """/**
 * Background task definitions for DCN App
 */

export const SOS_BACKGROUND_TASK = 'dcn-sos-background-monitor';
export const MESH_SCAN_TASK = 'dcn-mesh-scan';
export const DATA_SYNC_TASK = 'dcn-data-sync';

/**
 * Task configurations
 */
export const taskConfig = {
  [SOS_BACKGROUND_TASK]: {
    minimumInterval: 60, // 1 minute
    stopOnTerminate: false,
    startOnBoot: true,
  },
  [MESH_SCAN_TASK]: {
    minimumInterval: 30, // 30 seconds
    stopOnTerminate: false,
  },
  [DATA_SYNC_TASK]: {
    minimumInterval: 300, // 5 minutes
    stopOnTerminate: false,
  },
};
"""

with open(f'{app_dir}/src/services/backgroundTasks.ts', 'w') as f:
    f.write(bg_tasks)

# src/services/api.ts
api_service = """import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE = 'https://api.dcn.network/v1';

class ApiService {
  private async getHeaders() {
    const token = await AsyncStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  async get(endpoint: string) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: await this.getHeaders(),
    });
    return response.json();
  }

  async post(endpoint: string, body: any) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: await this.getHeaders(),
      body: JSON.stringify(body),
    });
    return response.json();
  }

  async delete(endpoint: string) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'DELETE',
      headers: await this.getHeaders(),
    });
    return response.json();
  }
}

export const api = new ApiService();
"""

with open(f'{app_dir}/src/services/api.ts', 'w') as f:
    f.write(api_service)

print("Service files created")
