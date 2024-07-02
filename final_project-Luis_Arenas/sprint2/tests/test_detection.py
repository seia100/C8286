import unittest
import asyncio
from src.detection.behavior_based import BehaviorBasedDetector, Packet
from src.detection.signature_based import SignatureBasedDetector

class TestDetection(unittest.TestCase):
    """
    Suite of tests for verifying the functionality of behavior-based and signature-based detection systems.
    """

    def setUp(self):
        """
        Setup method to initialize the detector instances before each test method is executed.
        """
        # Initialize the behavior-based detector
        self.behavior_detector = BehaviorBasedDetector()
        # Initialize the signature-based detector
        self.signature_detector = SignatureBasedDetector()

    def test_behavior_based_detection(self):
        """
        Test the behavior-based detection system with simulated network traffic.
        """
        async def run_test():
            # Simulate normal traffic
            for _ in range(500):
                await self.behavior_detector.update_stats(Packet(src_ip='192.168.1.1', dst_port=80, length=100))
            
            # Simulate anomalous traffic
            for _ in range(1500):
                await self.behavior_detector.update_stats(Packet(src_ip='192.168.1.2', dst_port=12345, length=1000))
            
            # Detect anomalies based on the simulated traffic
            result = await self.behavior_detector.detect_anomalies()
            # Check if the IP with anomalous behavior is correctly identified
            self.assertIn('192.168.1.2', result.anomalous_ips)
            # Ensure that normal behavior is not flagged as anomalous
            self.assertNotIn('192.168.1.1', result.anomalous_ips)
            # Check for the specific type of anomaly detected
            self.assertTrue(any("High packet count" in reason for reason in result.reasons['192.168.1.2']))

        # Run the asynchronous test using asyncio.run
        asyncio.run(run_test())

    def test_signature_based_detection(self):
        """
        Test the signature-based detection system with various packet payloads.
        """
        # Normal HTTP request, which should not trigger any signatures
        normal_packet = {'payload': 'GET /index.html HTTP/1.1'}
        # SQL Injection attempt, which should trigger a signature
        sql_injection_packet = {'payload': "GET /login.php?username=admin' OR '1'='1"}
        # Cross-Site Scripting attempt, which should also trigger a signature
        xss_packet = {'payload': '<script>alert("XSS")</script>'}
        
        # Assert that no signatures are detected for normal traffic
        self.assertEqual(len(self.signature_detector.detect(normal_packet)), 0)
        # Assert that SQL Injection is detected
        self.assertIn('SQL Injection', self.signature_detector.detect(sql_injection_packet))
        # Assert that XSS is detected
        self.assertIn('Cross-Site Scripting (XSS)', self.signature_detector.detect(xss_packet))

if __name__ == '__main__':
    unittest.main()
