1. Encapsulation / 内部状态暴露相关
1.1 ArrayIsStoredDirectly
Step 1：找到形如 this.field = paramArray; 或构造函数中直接保存入参数组到字段的地方。
Step 2：将赋值改为 this.field = paramArray.clone(); 或 Arrays.copyOf(...)，确保保存的是副本。
Step 3：如果字段类型是数组，但只在单个方法中使用，考虑将字段下沉为方法内局部变量。

1.2 MethodReturnsInternalArray
Step 1：找到方法返回内部数组字段 return this.field;。
Step 2：改为返回副本 return this.field.clone(); 或 Arrays.copyOf(...)。
Step 3：如有性能顾虑，可只对 public/protected 方法做此改动，private 方法可以保留。

1.3 ArrayIsStoredDirectly（构造函数版本，对应 allowPrivate=false 时）
Step 1：在非 private 构造函数 / 方法中查找 this.field = paramArray;。
Step 2：改成 this.field = paramArray != null ? paramArray.clone() : null;，避免 NPE。

这条其实和 1.1 是同一规则的细化版本，可以在实现里合在一起。

1.4 AccessorClassGeneration

Step 1：定位“外部类 new 内部类 + 内部类构造器为 private”的模式：

外部类方法中 new Inner()

Inner 是非静态内部类，且构造器是 private。

Step 2：将内部类构造器改为 package-private 或 protected，消除编译器生成 accessor class 的需求。

Step 3：如无必要嵌套结构，可将内部类提取为独立顶层类或静态内部类。

1.5 AccessorMethodGeneration

Step 1：找到外部类使用 OuterClass.this.privateField 或 OuterClass.this.privateMethod() 的地方。

Step 2：将这些被访问的成员由 private 调整为 package-private（去掉 private 即可）。

Step 3：如不希望改变可见性，则考虑将逻辑移动到公共的 helper 方法中，由外部间接调用。

1.6 AbstractClassWithoutAbstractMethod

Step 1：找到没有任何 abstract 方法的 abstract class。

Step 2（方案 A）：如果只是用作“基类且不希望被直接实例化”，保留 abstract，同时添加 protected 构造函数（禁止外部直接 new）。

Step 3（方案 B）：如果可以被实例化，则去掉 abstract 关键字，将其变为普通类。

1.7 ConstantsInInterface

Step 1：定位 interface 内的 public static final 字段。

Step 2：创建一个常量类 XxxConstants 或 enum。

Step 3：将 interface 内常量移动到常量类/枚举中，并替换所有引用为 XxxConstants.CONST_NAME 或 EnumType.CONST。

2. 资源 / 对象生命周期相关
2.1 AvoidMessageDigestField

Step 1：查找类型为 MessageDigest 的字段，且在多个方法中复用。

Step 2：将字段删除，在每个使用点改为方法内局部变量：

MessageDigest md = MessageDigest.getInstance("SHA-256");

Step 3：如必须共享（性能要求），则添加同步或使用线程本地变量；但对于自动重构，优先采用“局部新建”方案。

2.2 AvoidStringBufferField

Step 1：查找 StringBuffer / StringBuilder 类型的实例字段。

Step 2：如果该字段仅在某个方法中用于构建临时字符串：

删除字段定义，将其改为该方法内部的 StringBuilder 局部变量；

方法末尾用 toString() 产生结果。

Step 3：如果确实需要复用缓冲区，可将字段改为局部变量 + 将结果缓存到 String 字段，而不是持有可增长的 buffer。

2.3 UseTryWithResources

Step 1：识别 try { ... resource.close(); } finally { ... } 或 try/finally 手工关闭资源的代码（如 InputStream, Reader, Connection）。

Step 2：将资源声明移入 try (Resource r = ...) { ... } 结构中，删除显式 close() 调用和 finally 中仅负责关闭的代码。

Step 3：保证异常处理逻辑（例如日志打印）保留在 catch 或 finally（如还有其它逻辑）里。

2.4 PreserveStackTrace

Step 1：找到 catch 块中直接 new 并抛出新异常、但未传入原异常的代码：

catch (Exception e) { throw new OtherException("msg"); }

Step 2：改为将原异常作为 cause 传入：

throw new OtherException("msg", e);

Step 3：如果自定义异常类尚未有带 cause 的构造函数，为其添加一个 (String, Throwable) 或 (Throwable) 的构造函数。

2.5 AvoidPrintStackTrace

Step 1：查找 e.printStackTrace(); 及类似直接打印的方法调用。

Step 2：将其替换为日志记录，例如：logger.error("...", e);。

Step 3：如果当前类没有 logger 字段，则自动添加一个标准 logger 声明（如 SLF4J 的 private static final Logger LOGGER = LoggerFactory.getLogger(...);）。

3. 参数 / 变量修改相关
3.1 AvoidReassigningParameters

Step 1：找出方法/构造函数中对形参的赋值 param = ...;。

Step 2：引入一个新的局部变量：

Type newName = ...;，将后续使用 param 的地方改用 newName。

Step 3：删除对形参的重新赋值，确保参数保持“只读”语义。

3.2 AvoidReassigningCatchVariables

Step 1：在 catch (Exception e) { ... } 块中找到对 e 的重新赋值 e = new ...;。

Step 2：引入一个新的局部变量，如 Exception wrapped = new ...;，并使用该新变量。

Step 3：对于重新抛出的场景，使用 throw wrapped; 或 throw new ... (msg, e); 的模式。

3.3 AvoidReassigningLoopVariables

Step 1：在 for 或 foreach 中，查找对循环控制变量的写操作 i = ...;，或 item = ...;。

Step 2：改为使用单独的局部变量进行派生计算：

int tmp = i + 1; / var processed = item.trim();

Step 3：只有在确实需要更新控制逻辑且语义明确时，才保留赋值；否则保持循环变量单调更新。

3.4 UnusedAssignment

Step 1：找到对某变量的赋值，其后的代码中从未读取该变量值。

Step 2：如果赋值表达式无副作用（纯计算），直接删除该赋值语句。

Step 3：如果有副作用（函数调用），则将副作用表达式保留成独立语句，去掉无用的变量。

4. Unused / Dead Code 相关
4.1 UnusedLocalVariable

Step 1：定位从未被读取的局部变量声明。

Step 2：如果初始化表达式无副作用，删除变量声明整行。

Step 3：如果有副作用，则改为只保留副作用表达式，删除变量部分。

4.2 UnusedFormalParameter

Step 1：找到方法/构造函数中未被使用的参数。

Step 2：若该方法是 private 且只在本类中调用：

删除该参数，并同步更新所有调用点。

Step 3：若是对外接口（public/protected/接口实现），则可以保留参数，但可在实现中添加注释或 @SuppressWarnings("unused")，自动重构时建议仅对 private 方法做删除参数。

4.3 UnusedPrivateField

Step 1：查找从未被读取的 private 字段。

Step 2：确认无反射/序列化特例（自动工具一般跳过 serialVersionUID、LOGGER 等常见字段）。

Step 3：删除字段及仅用于给该字段赋值的语句。

4.4 UnusedPrivateMethod

Step 1：查找从未被调用的 private 方法。

Step 2：确认没有通过反射调用的迹象（例如字符串形式的方法名）。

Step 3：删除该方法定义；如果调用点曾经存在但被删除，应确保类仍能编译。

5. API 使用习惯 / Idiomatic Java
5.1 UseCollectionIsEmpty

Step 1：定位 collection.size() == 0 或 collection.size() != 0 等空检查。

Step 2：分别改为 collection.isEmpty() 或 !collection.isEmpty()。

Step 3：对于 > 0 / == 0 类型表达式，统一替换为 isEmpty 变体。

5.2 UseEnumCollections

Step 1：查找 Map<EnumType, ...> / Set<EnumType> 且实现类为 HashMap / HashSet。

Step 2：将声明修改为 EnumMap<EnumType, ...> 或 EnumSet<EnumType>，同时修改初始化：

new EnumMap<>(EnumType.class) / EnumSet.noneOf(EnumType.class)。

Step 3：保留键/值逻辑不变，确保 API 使用方式兼容。

5.3 ForLoopCanBeForeach

Step 1：识别典型的下标遍历：for (int i=0; i<list.size(); i++) { list.get(i) ... }。

Step 2：改为 for (ElementType e : list) { ... }，将 list.get(i) 替换为 e。

Step 3：如果循环内使用了 i 做其它作用（例如索引参与计算），则跳过重构。

5.4 ForLoopVariableCount

Step 1：检测 for 语句中初始化多个控制变量：for (int i=0, j=0; ...)。

Step 2：保留一个主变量 i，将其它变量 j 等移出为循环体中的局部变量或重新计算。

Step 3：如果多个控制变量确实不可分，则自动重构标记为 skip。

5.5 LiteralsFirstInComparisons

Step 1：寻找 obj.equals("literal") 反向写法 obj == "literal" 或 someObj.equals("x") 中可能 NPE 的顺序。

Step 2：改为 "literal".equals(obj)；

Step 3：对于 == 比较对象的情况，考虑是否可以改为 equals，否则保留（可能是身份比较）。

注意：PMD 这个 rule 主要针对常量放在左边防止 NPE；自动重构时要谨慎用在 == 上。

5.6 LooseCoupling

Step 1：识别依赖具体实现类型的字段/局部变量，例如 ArrayList, HashMap。

Step 2：将变量声明的类型替换为接口类型，如 List, Map。

Step 3：保留构造时的具体实现类型：new ArrayList<>() 不必强行改动。

5.7 MissingOverride

Step 1：查找重写父类或接口方法、但缺少 @Override 注解的方法。

Step 2：在方法签名前添加 @Override。

Step 3：保证 import 正确（通常不需要，因为 Override 在 java.lang）。

5.8 ImplicitFunctionalInterface

Step 1：Locate interfaces with exactly one abstract method，但没有 @FunctionalInterface。

Step 2：如果本意就是函数式接口，添加 @FunctionalInterface 注解。

Step 3：如果本意不是函数式接口，则自动重构可以选择跳过，或添加 @SuppressWarnings("PMD.ImplicitFunctionalInterface")，实际使用中建议只做提示。

6. I/O / Charset / 日志 等
6.1 RelianceOnDefaultCharset

Step 1：查找涉及 charset 的 I/O 调用但未显式传入 charset，比如 new String(bytes)、getBytes()、new InputStreamReader(in)。

Step 2：添加显式的 charset 参数，例如 StandardCharsets.UTF_8：

new String(bytes, StandardCharsets.UTF_8)

str.getBytes(StandardCharsets.UTF_8)

Step 3：如果项目已有统一封装工具类，优先替换为该工具方法，而不是直接传 charset 字面量。

6.2 GuardLogStatement

Step 1：针对字符串拼接比较重的日志语句 log.debug("x "+a+" y "+b)，检查是否缺少 log.isDebugEnabled() 守卫。

Step 2（方案 A）：在外层包一层：

if (log.isDebugEnabled()) { log.debug(...); }

Step 3（方案 B，推荐）：改成参数化日志：

log.debug("x {} y {}", a, b);，从而避免拼接开销。

7. 其它小规则
7.1 PrimitiveWrapperInstantiation

Step 1：查找 new 包装类实例，如 new Integer(1)、new Long(1L)。

Step 2：替换为 Integer.valueOf(1) 或使用自动装箱 Integer x = 1;。

Step 3：保留语义不变的前提下，避免显式 new。

7.2 UnnecessaryVarargsArrayCreation

Step 1：定位向 varargs 方法传入显式数组，如 foo(new String[]{"a", "b"})，而方法签名为 foo(String... args)。

Step 2：改为直接传可变参数：foo("a", "b")。

Step 3：如果调用处是动态构造数组且数量不固定，则保留现状。

7.3 CheckResultSet

Step 1：查找 ResultSet 导航方法调用（next(), first(), 等）后直接使用结果，而没有检查返回值。

Step 2：将调用改为：

if (rs.next()) { ... use rs ... } else { ... handle empty ... }

Step 3：对于自动重构，else 分支可以先插入一个 // TODO handle empty result 注释，避免改变控制流太多。

7.4 DefaultLabelNotLastInSwitch

Step 1：在 switch 中找到非最后一个 default 分支。

Step 2：在不改变 case 执行顺序语义的前提下，将 default case 移动到最后。

Step 3：如果 case 之间存在 fall-through（缺少 break），则自动重构谨慎：可先插入注释而不做调整。
