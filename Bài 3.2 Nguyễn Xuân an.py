using System;

namespace EmployeeHierarchy
{
    // 1. Lớp cha Person
    public class Person
    {
        // Properties
        public string Id { get; init; }
        public string FullName { get; set; }
        public int BirthYear { get; set; }

        // Constructor
        public Person(string id, string fullName, int birthYear)
        {
            Id = id;
            FullName = fullName;
            BirthYear = birthYear;
        }

        // Method tính tuổi
        public int GetAge(int currentYear)
        {
            return currentYear - BirthYear;
        }
    }

    // 2. Lớp con Employee kế thừa từ Person
    public class Employee : Person
    {
        // Thuộc tính lương cơ bản
        public decimal BaseSalary { get; set; }

        // Constructor ủy quyền gọi constructor của Person thông qua từ khóa base
        public Employee(string id, string fullName, int birthYear, decimal baseSalary)
            : base(id, fullName, birthYear)
        {
            BaseSalary = baseSalary;
        }

        // Phương thức tính thu nhập (được đánh dấu virtual để cho phép lớp con ghi đè)
        public virtual decimal CalculateIncome()
        {
            return BaseSalary;
        }
    }

    // 3. Lớp con Manager kế thừa từ Employee và đánh dấu sealed
    public sealed class Manager : Employee
    {
        // Thuộc tính phụ cấp trách nhiệm
        public decimal ResponsibilityAllowance { get; set; }

        // Constructor nhận các tham số và gọi constructor của lớp Employee qua base
        public Manager(string id, string fullName, int birthYear, decimal baseSalary, decimal allowance)
            : base(id, fullName, birthYear, baseSalary)
        {
            ResponsibilityAllowance = allowance;
        }

        // Ghi đè phương thức CalculateIncome
        public override decimal CalculateIncome() => BaseSalary + ResponsibilityAllowance;
    }

    /*
     * GIẢI THÍCH TẠI SAO KHÔNG THỂ TẠO LỚP KẾ THỪA TỪ MANAGER:
     * 
     * Lớp Manager được khai báo với từ khóa 'sealed' (public sealed class Manager).
     * Từ khóa 'sealed' trong C# dùng để "khóa" lớp lại, ngăn không cho bất kỳ lớp nào 
     * khác kế thừa từ nó.
     * 
     * Ví dụ: Nếu cố tình khai báo `public class SeniorManager : Manager` 
     * trình biên dịch (Compiler) sẽ báo lỗi:
     * "CS0509: 'SeniorManager': cannot derive from sealed type 'Manager'".
     */

    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            int currentYear = DateTime.Now.Year;

            // Khởi tạo 1 đối tượng Employee và 1 đối tượng Manager
            Employee emp = new Employee("EMP001", "Nguyễn Văn Anh", 1995, 12000000m);
            Manager mgr = new Manager("MGR001", "Trần Thị Bình", 1988, 25000000m, 8000000m);

            Console.WriteLine("================ PHIẾU LƯƠNG NHÂN VIÊN ================");
            PrintPaySlip(emp, currentYear);

            Console.WriteLine("\n================ PHIẾU LƯƠNG QUẢN LÝ ================");
            PrintPaySlip(mgr, currentYear);
        }

        // Hàm hỗ trợ in phiếu lương
        private static void PrintPaySlip(Employee employee, int currentYear)
        {
            Console.WriteLine($"Mã định danh : {employee.Id}");
            Console.WriteLine($"Họ và tên    : {employee.FullName}");
            Console.WriteLine($"Tuổi         : {employee.GetAge(currentYear)}");
            Console.WriteLine($"Lương cơ bản : {employee.BaseSalary:N0} VNĐ");
            Console.WriteLine($"Thu nhập     : {employee.CalculateIncome():N0} VNĐ");
            Console.WriteLine("---------------------------------------------------");
        }
    }
}