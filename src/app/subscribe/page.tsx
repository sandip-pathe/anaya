"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import Link from "next/link";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Logo from "@/components/landing/logo";
import { addSubscription } from "./actions";
import { Trigger } from "@radix-ui/react-select";

// Updated form schema with new fields and purpose values
const formSchema = z
  .object({
    purpose: z.enum(["wishlistFree", "wishlistPaid", "question"]),
    fullName: z.string().min(1, "Full name is required"),
    email: z.string().email({ message: "Please enter a valid email address." }),
    company: z.string().optional(),
    jobTitle: z.string().optional(),
    teamSize: z.string().optional(),
    source: z.string().optional(),
    challenges: z.string().optional(),
    urgency: z.string().optional(),
    cardNumber: z.string().optional(),
    expiry: z.string().optional(),
    cvc: z.string().optional(),
    questionText: z.string().optional(),
  })
  .superRefine((data, ctx) => {
    if (data.purpose === "wishlistPaid") {
      if (!data.cardNumber) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["cardNumber"],
          message: "Card number is required",
        });
      }
      if (!data.expiry) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["expiry"],
          message: "Expiry date is required",
        });
      }
      if (!data.cvc) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["cvc"],
          message: "CVC is required",
        });
      }
    } else if (data.purpose === "question") {
      if (!data.questionText) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["questionText"],
          message: "Question is required",
        });
      }
    }
  });

export type FormValues = z.infer<typeof formSchema>;

// Define InputField props interface
interface InputFieldProps {
  name: keyof FormValues;
  label: string;
  placeholder?: string;
  form: any;
}

// Define InputField as a standalone component
const InputField: React.FC<InputFieldProps> = ({
  form,
  name,
  label,
  placeholder,
}) => (
  <FormField
    control={form.control}
    name={name}
    render={({ field }) => (
      <FormItem className="w-full text-base">
        <FormLabel className="text-base">{label}</FormLabel>
        <FormControl>
          <Input
            className="placeholder:text-base"
            placeholder={placeholder}
            {...field}
            value={field.value ?? ""}
          />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
);

export default function EarlyAccessPage() {
  const { toast } = useToast();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      purpose: "wishlistFree",
      fullName: "",
      email: "",
      company: "",
      jobTitle: "",
      teamSize: undefined,
      source: "",
      challenges: "",
      urgency: undefined,
      cardNumber: "",
      expiry: "",
      cvc: "",
      questionText: "",
    },
  });

  const watchPurpose = form.watch("purpose");

  const onSubmit = async (data: FormValues) => {
    try {
      await addSubscription(data);
      toast({
        title: "Success!",
        description:
          data.purpose === "wishlistPaid"
            ? "You've joined our priority wishlist! Payment processed successfully."
            : data.purpose === "wishlistFree"
            ? "You've been added to our wishlist!"
            : "Your question has been submitted! We'll contact you soon.",
      });
      form.reset();
    } catch (error) {
      console.error("Submission failed:", error);
      toast({
        variant: "destructive",
        title: "Submission Failed",
        description:
          "There was a problem submitting your request. Please try again.",
      });
    }
  };

  return (
    <>
      <div className="min-h-screen grid grid-cols-1 lg:grid-cols-2">
        <div className="flex flex-col px-8 bg-[#fffaf5] h-full overflow-y-auto my-auto">
          <div className="max-w-lg mx-auto w-full space-y-4 py-8">
            <Logo />
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-6"
              >
                {/* Common Fields */}
                <div className="space-y-4">
                  <div className="flex flex-col md:flex-row gap-4 w-full">
                    <InputField
                      form={form}
                      name="fullName"
                      label="Full Name"
                      placeholder="Your name"
                    />
                    <InputField
                      form={form}
                      name="email"
                      label="Email"
                      placeholder="you@example.com"
                    />
                  </div>
                  <div className="flex flex-col md:flex-row gap-4 w-full">
                    <InputField
                      form={form}
                      name="company"
                      label="Company (optional)"
                      placeholder="Your company"
                    />
                    <InputField
                      form={form}
                      name="jobTitle"
                      label="Job Title (optional)"
                      placeholder="Your role"
                    />
                  </div>

                  <FormField
                    control={form.control}
                    name="teamSize"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-base">
                          Team Size (optional)
                        </FormLabel>
                        <Select
                          onValueChange={field.onChange}
                          defaultValue={field.value}
                        >
                          <FormControl>
                            <SelectTrigger className="text-base">
                              <SelectValue placeholder="Select team size" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="1-10" className="text-base">
                              1-10
                            </SelectItem>
                            <SelectItem value="11-50" className="text-base">
                              11-50
                            </SelectItem>
                            <SelectItem value="51-200" className="text-base">
                              51-200
                            </SelectItem>
                            <SelectItem value="201-500" className="text-base">
                              201-500
                            </SelectItem>
                            <SelectItem value="500+" className="text-base">
                              500+
                            </SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Conditional Fields for Wishlist */}
                {(watchPurpose === "wishlistFree" ||
                  watchPurpose === "wishlistPaid") && (
                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      name="challenges"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-base">
                            What challenges are you trying to solve?
                          </FormLabel>
                          <FormControl>
                            <Textarea
                              placeholder="Your answer"
                              {...field}
                              value={field.value ?? ""}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="urgency"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-base">
                            How important is this for you?
                          </FormLabel>
                          <Select
                            onValueChange={field.onChange}
                            defaultValue={field.value}
                          >
                            <FormControl>
                              <SelectTrigger className="text-base">
                                <SelectValue placeholder="Select urgency" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              <SelectItem
                                value="notUrgent"
                                className="text-base"
                              >
                                Not urgent
                              </SelectItem>
                              <SelectItem value="soon" className="text-base">
                                Soon
                              </SelectItem>
                              <SelectItem
                                value="veryUrgent"
                                className="text-base"
                              >
                                Very urgent
                              </SelectItem>
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    {/* Purpose Selection - Now inside Join Wishlist tab */}
                    {(watchPurpose === "wishlistFree" ||
                      watchPurpose === "wishlistPaid") && (
                      <FormField
                        control={form.control}
                        name="purpose"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-lg text-gray-800 mb-2">
                              Join Wishlist
                            </FormLabel>
                            <FormControl>
                              <RadioGroup
                                onValueChange={field.onChange}
                                value={field.value}
                                className="flex flex-col space-y-2"
                              >
                                <FormItem className="flex items-center space-x-2">
                                  <FormControl>
                                    <RadioGroupItem value="wishlistFree" />
                                  </FormControl>
                                  <FormLabel className="cursor-pointer text-base">
                                    Join Free
                                  </FormLabel>
                                </FormItem>
                                <FormItem className="flex items-center space-x-2">
                                  <FormControl>
                                    <RadioGroupItem value="wishlistPaid" />
                                  </FormControl>
                                  <FormLabel className="cursor-pointer text-base">
                                    Priority Access ($10 Refundable)
                                  </FormLabel>
                                </FormItem>
                              </RadioGroup>
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    )}

                    {watchPurpose === "wishlistPaid" && (
                      <Card className="bg-gray-50 border border-gray-200 rounded-lg">
                        <CardHeader className="pb-4">
                          <CardTitle className="flex justify-between items-center text-base">
                            <span>Payment Amount</span>
                            <span className="font-bold text-blue-600">
                              $10.00 USD
                            </span>
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <InputField
                            form={form}
                            name="cardNumber"
                            label="Card Number"
                            placeholder="1234 5678 9012 3456"
                          />
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <InputField
                              form={form}
                              name="expiry"
                              label="Expiry Date"
                              placeholder="MM/YY"
                            />
                            <InputField
                              form={form}
                              name="cvc"
                              label="CVC"
                              placeholder="123"
                            />
                          </div>
                          <p className="text-sm text-gray-500 mt-2">
                            Fully refundable anytime before launch.
                          </p>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                )}

                {/* Submit Button */}
                <Button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg text-base"
                  disabled={form.formState.isSubmitting}
                >
                  {form.formState.isSubmitting
                    ? "Submitting..."
                    : watchPurpose === "wishlistPaid"
                    ? "Join Wishlist (Priority)"
                    : watchPurpose === "wishlistFree"
                    ? "Join Wishlist"
                    : "Submit Question"}
                </Button>

                <p className="text-center text-xs text-gray-500 mt-4">
                  By submitting, you agree to our{" "}
                  <Link
                    href="/privacy"
                    className="text-blue-500 underline hover:text-blue-700"
                  >
                    Privacy Policy
                  </Link>
                  .
                </p>
              </form>
            </Form>
          </div>
        </div>

        {/* Right: Image */}
        <div className="hidden lg:flex flex-col justify-center items-center relative bg-black h-full">
          {/* Content container */}
          <div className="relative z-10 text-center px-8">
            <h1 className="font-headline text-5xl tracking-tight text-foreground font-bold mb-4 text-white">
              Join the Innovation Wave
            </h1>
            <p className="text-lg text-blue-100 max-w-md mx-auto">
              "Being an early adopter gave us a competitive edge we couldn't
              have gotten anywhere else."
            </p>
            <div className="mt-4 text-blue-100 italic">
              - Sarah K., Product Director at TechCorp
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
