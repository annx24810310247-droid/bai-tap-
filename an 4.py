using System;

namespace PaymentSystem
{
    // =========================================================================
    // 1. DỊCH VỤ INTERFACES (NĂNG LỰC - "CAN-DO")
    // =========================================================================
    public interface IPayable
    {
        bool ProcessPayment(decimal amount);
    }

    public interface IRefundable
    {
        bool ProcessRefund(decimal amount, string reason);
    }

    // =========================================================================
    // 2. LỚP TRỪU TƯỢNG PAYMENTGATEWAY (BẢN CHẤT - "IS-A")
    // =========================================================================
    public abstract class PaymentGateway
    {
        public string TransactionId { get; init; }
        public DateTime CreationDate { get; init; }
        public string Status { get; protected set; }

        protected PaymentGateway(string transactionId)
        {
            TransactionId = transactionId;
            CreationDate = DateTime.Now;
            Status = "Pending";
        }

        // Phương thức trừu tượng - Bắt buộc các lớp con phải cài đặt chi tiết
        public abstract void ValidateConnection();

        // Phương thức thông thường - Cung cấp sẵn logic dùng chung
        public virtual void LogTransaction(string message)
        {
            Console.WriteLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] [Mã GD: {TransactionId}] [{Status}] - {message}");
        }
    }

    // =========================================================================
    // 3. LỚP CỤ THỂ MOMOPAYMENT
    // =========================================================================
    public class MomoPayment : PaymentGateway, IPayable, IRefundable
    {
        public string PhoneNumber { get; set; }

        public MomoPayment(string transactionId, string phoneNumber) 
            : base(transactionId)
        {
            PhoneNumber = phoneNumber;
        }

        // Thực thi phương thức trừu tượng từ lớp cha PaymentGateway
        public override void ValidateConnection()
        {
            Console.WriteLine($"[MoMo API] Đang kiểm tra kết nối cho SĐT: {PhoneNumber}...");
            Console.WriteLine("[MoMo API] Kết nối thành công tới cổng thanh toán MoMo.");
        }

        // Triển khai Interface IPayable
        public bool ProcessPayment(decimal amount)
        {
            if (amount <= 0)
            {
                LogTransaction("Thanh toán thất bại: Số tiền không hợp lệ.");
                return false;
            }

            Status = "Success";
            LogTransaction($"Thanh toán thành công số tiền {amount:N0} VNĐ qua ví MoMo ({PhoneNumber}).");
            return true;
        }

        // Triển khai Interface IRefundable
        public bool ProcessRefund(decimal amount, string reason)
        {
            if (amount <= 0)
            {
                LogTransaction("Hoàn tiền thất bại: Số tiền hoàn phải lớn hơn 0.");
                return false;
            }

            Status = "Refunded";
            LogTransaction($"Hoàn tiền thành công {amount:N0} VNĐ. Lý do: {reason}");
            return true;
        }
    }

    // =========================================================================
    // 4. KỊCH BẢN KIỂM THỬ (MAIN)
    // =========================================================================
    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            Console.WriteLine("=== KHỞI TẠO VÀ KIỂM TRA CỔNG THANH TOÁN MOMO ===");
            MomoPayment momoApp = new MomoPayment("MM-20260909-001", "0987654321");
            
            // Kiểm tra kết nối
            momoApp.ValidateConnection();
            Console.WriteLine();

            // Ép kiểu sang Interface IPayable để xử lý thanh toán độc lập
            Console.WriteLine("=== THỰC HIỆN THANH TOÁN (QUA INTERFACE IPAYABLE) ===");
            IPayable payableService = momoApp;
            bool isPaid = payableService.ProcessPayment(450000m);

            Console.WriteLine();

            // Ép kiểu sang Interface IRefundable để xử lý hoàn tiền độc lập
            Console.WriteLine("=== THỰC HIỆN HOÀN TIỀN (QUA INTERFACE IREFUNDABLE) ===");
            if (isPaid)
            {
                IRefundable refundableService = momoApp;
                refundableService.ProcessRefund(450000m, "Khách hàng hủy đơn hàng");
            }

            Console.WriteLine("\n=== TRẠNG THÁI GIAO DỊCH CUỐI CÙNG ===");
            Console.WriteLine($"Mã giao dịch : {momoApp.TransactionId}");
            Console.WriteLine($"Số điện thoại : {momoApp.PhoneNumber}");
            Console.WriteLine($"Trạng thái   : {momoApp.Status}");
        }
    }
}