using System;
using System.Collections.Generic;

namespace PolymorphismDemo
{
    // =========================================================================
    // 1. METHOD OVERLOADING (ĐA HÌNH TẠI THỜI ĐIỂM BIÊN DỊCH)
    // =========================================================================
    public static class DiscountCalculator
    {
        // Version 1: Giảm mặc định 5%
        public static decimal ApplyDiscount(decimal totalAmount)
        {
            return totalAmount * 0.95m;
        }

        // Version 2: Giảm theo phần trăm tùy biến (0 - 100%)
        public static decimal ApplyDiscount(decimal totalAmount, double percentage)
        {
            if (percentage < 0 || percentage > 100)
            {
                throw new ArgumentOutOfRangeException(nameof(percentage), "Phần trăm giảm giá phải từ 0 đến 100.");
            }
            decimal discountRate = (decimal)percentage / 100m;
            return totalAmount * (1 - discountRate);
        }

        // Version 3: Giảm theo số tiền cố định nếu đơn hàng đạt giá trị tối thiểu
        public static decimal ApplyDiscount(decimal totalAmount, decimal fixedVoucher, decimal minimumOrder)
        {
            if (totalAmount >= minimumOrder)
            {
                decimal result = totalAmount - fixedVoucher;
                return result < 0 ? 0 : result;
            }
            return totalAmount;
        }
    }

    // =========================================================================
    // 2. METHOD OVERRIDING (ĐA HÌNH TẠI THỜI ĐIỂM THỰC THI)
    // =========================================================================
    
    // Lớp cha DeliveryService
    public class DeliveryService
    {
        public string OrderId { get; init; }
        public double DistanceKm { get; set; }

        public DeliveryService(string orderId, double distanceKm)
        {
            OrderId = orderId;
            DistanceKm = distanceKm;
        }

        // Phương thức virtual cho phép lớp con ghi đè
        public virtual decimal CalculateShippingFee()
        {
            return (decimal)DistanceKm * 5000m;
        }
    }

    // Lớp con: Giao hàng siêu tốc
    public class ExpressDelivery : DeliveryService
    {
        public ExpressDelivery(string orderId, double distanceKm) 
            : base(orderId, distanceKm) { }

        // Ghi đè tính phí: 1.5x phí cơ bản + 20.000 VNĐ phụ phí
        public override decimal CalculateShippingFee()
        {
            decimal baseFee = base.CalculateShippingFee();
            return (baseFee * 1.5m) + 20000m;
        }
    }

    // Lớp con: Giao hàng tiết kiệm
    public class EcoDelivery : DeliveryService
    {
        public EcoDelivery(string orderId, double distanceKm) 
            : base(orderId, distanceKm) { }

        // Ghi đè tính phí: Giảm 10% nếu quãng đường > 10km
        public override decimal CalculateShippingFee()
        {
            decimal baseFee = base.CalculateShippingFee();
            if (DistanceKm > 10)
            {
                return baseFee * 0.9m;
            }
            return baseFee;
        }
    }

    // =========================================================================
    // 3. KỊCH BẢN KIỂM THỬ (MAIN)
    // =========================================================================
    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            // --- KIỂM THỬ OVERLOADING ---
            Console.WriteLine("=== 1. KIỂM THỬ OVERLOADING (DISCOUNT CALCULATOR) ===");
            decimal originalPrice = 1000000m; // 1.000.000 VNĐ

            decimal price1 = DiscountCalculator.ApplyDiscount(originalPrice);
            decimal price2 = DiscountCalculator.ApplyDiscount(originalPrice, 15.0); // Giảm 15%
            decimal price3 = DiscountCalculator.ApplyDiscount(originalPrice, 200000m, 500000m); // Voucher 200k cho đơn từ 500k

            Console.WriteLine($"Giá gốc                  : {originalPrice:N0} VNĐ");
            Console.WriteLine($"Giảm mặc định (5%)       : {price1:N0} VNĐ");
            Console.WriteLine($"Giảm tùy chỉnh (15%)     : {price2:N0} VNĐ");
            Console.WriteLine($"Giảm voucher (200,000 VNĐ): {price3:N0} VNĐ");

            // --- KIỂM THỬ OVERRIDING ---
            Console.WriteLine("\n=== 2. KIỂM THỬ OVERRIDING (RUNTIME POLYMORPHISM) ===");

            // Danh sách các dịch vụ vận chuyển chứa cả đối tượng lớp cha lẫn các lớp con
            List<DeliveryService> deliveries = new List<DeliveryService>
            {
                new DeliveryService("ORD-001", 12.0),
                new ExpressDelivery("ORD-002", 12.0),
                new EcoDelivery("ORD-003", 12.0),
                new EcoDelivery("ORD-004", 5.0)
            };

            // Duyệt danh sách để gọi phương thức đã được ghi đè tương ứng
            foreach (var delivery in deliveries)
            {
                string serviceTypeName = delivery.GetType().Name;
                decimal shippingFee = delivery.CalculateShippingFee();

                Console.WriteLine($"Đơn hàng: {delivery.OrderId} | Loại DV: {serviceTypeName,-15} | Khoảng cách: {delivery.DistanceKm} km | Phí ship: {shippingFee:N0} VNĐ");
            }
        }
    }
}