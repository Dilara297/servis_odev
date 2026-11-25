import sys
import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea


class AlanClient(Node):
    def __init__(self):
        super().__init__('alan_client')
        self.cli = self.create_client(RectangleArea, 'rectangle_area')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Servis bekleniyor...')

    def send_request(self, width, height):
        req = RectangleArea.Request()
        req.width = float(width)
        req.height = float(height)
        return self.cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 3:
        print('Kullanım: ros2 run alan_py alan_client <width> <height>')
        rclpy.shutdown()
        return

    client = AlanClient()
    future = client.send_request(sys.argv[1], sys.argv[2])
    rclpy.spin_until_future_complete(client, future)

    response = future.result()
    if response.success:
        client.get_logger().info(
            f'Başarılı! width={sys.argv[1]}, height={sys.argv[2]} -> Alan: {response.area}'
        )
    else:
        client.get_logger().error(
            f'Reddedildi! Negatif değer girilemez (width={sys.argv[1]}, height={sys.argv[2]})'
        )

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
